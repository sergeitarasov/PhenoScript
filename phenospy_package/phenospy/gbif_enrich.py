from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


# Match any .dwc-Taxon_ID_taxonID line
TAXON_ID_LINE_PATTERN = re.compile(
    r"""^(?P<indent>\s*)
        (?P<subject>[^\s]+)
        \s+\.dwc-Taxon_ID_taxonID\s+
        (?P<quote>['"])(?P<value>.*?)(?P=quote);
        \s*$
    """,
    re.VERBOSE,
)

GBIF_SPECIES_URL_PATTERN = re.compile(
    r"^https?://www\.gbif\.org/species/(?P<gbif_id>\d+)$"
)

# Order of inserted taxonomy lines
GBIF_TO_DWC = [
    ("canonicalName", ".dwc-Scientific_Name"),
    ("genus", ".dwc-Genus"),
    ("family", ".dwc-Family"),
    ("order", ".dwc-Order"),
    ("class", ".dwc-Class"),
    ("phylum", ".dwc-Phylum"),
    ("kingdom", ".dwc-Kingdom"),
]


def quote_single(value: str) -> str:
    value = str(value).replace("\\", "\\\\").replace("'", "\\'")
    return f"'{value}'"


def fetch_gbif_species(gbif_id: str, timeout: int = 20) -> dict:
    """Fetch one taxon record from the GBIF species API."""
    api_url = f"https://api.gbif.org/v1/species/{gbif_id}"
    with urlopen(api_url, timeout=timeout) as response:
        return json.load(response)


def make_taxonomy_line(indent: str, subject: str, predicate: str, value: str) -> str:
    return f"{indent}{subject} {predicate} {quote_single(value)};"


def subject_has_predicate_nearby(
    lines: list[str],
    start_idx: int,
    subject: str,
    predicate: str,
    window: int = 12,
) -> bool:
    """
    Avoid inserting duplicates if taxonomy was already added nearby.
    """
    end_idx = min(len(lines), start_idx + 1 + window)
    prefix = f"{subject} {predicate} "
    for i in range(start_idx + 1, end_idx):
        if lines[i].lstrip().startswith(prefix):
            return True
    return False


def extract_gbif_id_from_taxon_id_value(value: str) -> str | None:
    """
    Return GBIF numeric key if the taxonID value is a GBIF species URL.

    Examples:
      ott_id:3328193 -> None
      https://www.gbif.org/species/1094062 -> 1094062
    """
    m = GBIF_SPECIES_URL_PATTERN.match(value.strip())
    if m:
        return m.group("gbif_id")
    return None


def enrich_phs_text_with_gbif(
    text: str,
    *,
    timeout: int = 20,
    insert_blank_line: bool = True,
) -> str:
    """
    Enrich Phenoscript text with taxonomy fetched from GBIF.

    The function looks for consecutive .dwc-Taxon_ID_taxonID lines belonging to the
    same taxon subject, finds the first GBIF species URL among them, fetches GBIF
    taxonomy, and inserts missing taxonomy lines immediately after the taxonID block.

    Parameters
    ----------
    text
        Input Phenoscript text.
    timeout
        HTTP timeout in seconds for GBIF API requests.
    insert_blank_line
        Whether to add a blank line after inserted taxonomy lines.

    Returns
    -------
    str
        Enriched Phenoscript text.
    """
    lines = text.splitlines()
    output_lines: list[str] = []

    i = 0
    while i < len(lines):
        line = lines[i]
        output_lines.append(line)

        m = TAXON_ID_LINE_PATTERN.match(line)
        if not m:
            i += 1
            continue

        subject = m.group("subject")
        indent = m.group("indent")
        values = [m.group("value")]
        last_idx = i

        j = i + 1
        while j < len(lines):
            m2 = TAXON_ID_LINE_PATTERN.match(lines[j])
            if not m2 or m2.group("subject") != subject:
                break
            output_lines.append(lines[j])
            values.append(m2.group("value"))
            last_idx = j
            j += 1

        gbif_id = None
        for value in values:
            gbif_id = extract_gbif_id_from_taxon_id_value(value)
            if gbif_id:
                break

        if gbif_id:
            try:
                gbif_data = fetch_gbif_species(gbif_id, timeout=timeout)
            except (HTTPError, URLError, TimeoutError) as exc:
                print(f"Warning: could not fetch GBIF {gbif_id}: {exc}")
                i = j
                continue
            except Exception as exc:
                print(f"Warning: unexpected GBIF error for {gbif_id}: {exc}")
                i = j
                continue

            inserted_any = False
            for gbif_field, dwc_predicate in GBIF_TO_DWC:
                value = gbif_data.get(gbif_field)
                if not value:
                    continue

                if subject_has_predicate_nearby(lines, last_idx, subject, dwc_predicate):
                    continue

                output_lines.append(
                    make_taxonomy_line(indent, subject, dwc_predicate, str(value))
                )
                inserted_any = True

            if inserted_any and insert_blank_line:
                output_lines.append("")

        i = j

    return "\n".join(output_lines) + "\n"


def enrich_phs_file_with_gbif(
    input_path: str | Path,
    output_path: str | Path | None = None,
    *,
    timeout: int = 20,
    insert_blank_line: bool = True,
) -> str:
    """
    Read a .phs file, enrich it using GBIF taxonomy, and optionally write output.

    Parameters
    ----------
    input_path
        Path to the input .phs file.
    output_path
        Path to write the enriched .phs file. If None, the file is not written.
    timeout
        HTTP timeout in seconds for GBIF API requests.
    insert_blank_line
        Whether to add a blank line after inserted taxonomy lines.

    Returns
    -------
    str
        Enriched Phenoscript text.
    """
    input_path = Path(input_path)
    text = input_path.read_text(encoding="utf-8")

    enriched = enrich_phs_text_with_gbif(
        text,
        timeout=timeout,
        insert_blank_line=insert_blank_line,
    )

    if output_path is not None:
        output_path = Path(output_path)
        output_path.write_text(enriched, encoding="utf-8")

    return enriched


def gbif_enrich_cli(args) -> None:
    """
    CLI entry point wrapper.
    """
    enrich_phs_file_with_gbif(
        input_path=args.phs_file,
        output_path=args.output_file,
        timeout=args.timeout,
        insert_blank_line=not args.no_blank_line,
    )
    print(f"Wrote {args.output_file}")