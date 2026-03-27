from __future__ import annotations

import random
import re
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, StrictUndefined

YAML_BLOCK_PATTERN = re.compile(
    r"^(?P<indent>[ \t]*)#>>>YAML(?:[ \t]+(?P<template_name>[A-Za-z0-9_\-]+))?[ \t]*\n"
    r"(?P<yaml>.*?)"
    r"^(?P=indent)#<<<YAML[ \t]*$",
    re.MULTILINE | re.DOTALL,
)


def load_yaml_file(path: str | Path) -> dict[str, Any]:
    """Load a YAML file and return its top-level mapping."""
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError(f"{path} did not parse to a mapping.")

    return data


def quote_single(value: str) -> str:
    value = str(value).replace("\\", "\\\\").replace("'", "\\'")
    return f"'{value}'"


def quote_double(value: str) -> str:
    value = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{value}"'


def quote_mixed(value: str) -> str:
    """
    Quote URLs with double quotes, everything else with single quotes.
    """
    value = str(value)
    if value.startswith(("http://", "https://")):
        return quote_double(value)
    return quote_single(value)


def make_jinja_env() -> Environment:
    env = Environment(undefined=StrictUndefined, trim_blocks=True, lstrip_blocks=True)
    env.globals["quote_single"] = quote_single
    env.globals["quote_double"] = quote_double
    env.globals["quote_mixed"] = quote_mixed
    return env


def get_nested(data: dict[str, Any], dotted_path: str) -> Any:
    """
    Supports paths like:
      specimen.id
      specimen..rdfs-label
      specimen..dwc-Taxon_ID

    A double dot means the key itself begins with '.'.
    """
    parts = dotted_path.split(".")
    cur: Any = data
    i = 0

    while i < len(parts):
        part = parts[i]

        if part == "":
            i += 1
            if i >= len(parts):
                raise KeyError(f"Invalid path: {dotted_path}")
            key = "." + parts[i]
        else:
            key = part

        if not isinstance(cur, dict) or key not in cur:
            raise KeyError(dotted_path)

        cur = cur[key]
        i += 1

    return cur


def has_nested(data: dict[str, Any], dotted_path: str) -> bool:
    try:
        get_nested(data, dotted_path)
        return True
    except KeyError:
        return False


def generate_id(prefix: str = "id-", length: int = 6, charset: str = "hex") -> str:
    """Generate a random identifier."""
    if charset == "hex":
        alphabet = "0123456789abcdef"
    else:
        raise ValueError(f"Unsupported charset: {charset}")

    return prefix + "".join(random.choice(alphabet) for _ in range(length))


def validate_required(data: dict[str, Any], required: list[str]) -> None:
    """Validate that all required dotted paths are present."""
    for path in required:
        if not has_nested(data, path):
            raise ValueError(f"Missing required field: {path}")


def validate_block_data(block_data: dict[str, Any]) -> None:
    """
    Apply block-specific validation rules that are not convenient to
    express in templates alone.
    """
    if "specimen" in block_data:
        specimen = block_data["specimen"]

        if ".is_a" in specimen:
            is_a = specimen[".is_a"]

            if not isinstance(is_a, list):
                raise ValueError("specimen..is_a must be a list.")

            if len(is_a) < 1:
                raise ValueError("specimen..is_a must contain at least one element.")

            for i, item in enumerate(is_a):
                if not isinstance(item, str) or not item.strip():
                    raise ValueError(f"specimen..is_a[{i}] must be a non-empty string.")


def render_template_block(
    block_data: dict[str, Any],
    template_spec: dict[str, Any],
    jinja_env: Environment | None = None,
) -> str:
    """
    Render a single parsed YAML block using one template spec.
    """
    if jinja_env is None:
        jinja_env = make_jinja_env()

    validate_required(block_data, template_spec.get("required", []))
    validate_block_data(block_data)

    context: dict[str, Any] = dict(block_data)

    if "specimen" in context and ".is_a" in context["specimen"]:
        is_a = context["specimen"][".is_a"]
        extra_classes = is_a[1:]
        context["extra_cls_annotations"] = "".join(
            f", cls = {quote_single(cls)}" for cls in extra_classes
        )
    else:
        context["extra_cls_annotations"] = ""

    for var_name, spec in template_spec.get("generated_ids", {}).items():
        context[var_name] = generate_id(
            prefix=spec.get("prefix", "id-"),
            length=int(spec.get("length", 6)),
            charset=spec.get("charset", "hex"),
        )

    for var_name, template_str in template_spec.get("vars", {}).items():
        template = jinja_env.from_string(template_str)
        context[var_name] = template.render(**context)

    output_lines: list[str] = []

    for entry in template_spec.get("lines", []):
        if isinstance(entry, str):
            template = jinja_env.from_string(entry)
            output_lines.append(template.render(**context))
            continue

        if not isinstance(entry, dict):
            raise ValueError(f"Invalid line entry: {entry}")

        if "if" in entry and not has_nested(block_data, entry["if"]):
            continue

        if "for_each" in entry:
            if not has_nested(block_data, entry["for_each"]):
                continue

            values = get_nested(block_data, entry["for_each"])

            if not isinstance(values, list):
                raise ValueError(f"{entry['for_each']} must be a list.")

            if not values:
                continue

            template = jinja_env.from_string(entry["template"])
            for item in values:
                output_lines.append(template.render(item=item, **context))
            continue

        if "template" in entry:
            template = jinja_env.from_string(entry["template"])
            output_lines.append(template.render(**context))
            continue

        raise ValueError(f"Unsupported line entry: {entry}")

    return "\n".join(output_lines)


def replace_yaml_blocks(
    source_text: str,
    templates: dict[str, Any],
    default_template_name: str = "default",
    jinja_env: Environment | None = None,
) -> str:
    """
    Replace all active #>>>YAML ... #<<<YAML blocks in source_text
    using the provided templates.
    """
    if jinja_env is None:
        jinja_env = make_jinja_env()

    def repl(match: re.Match[str]) -> str:
        indent = match.group("indent")
        template_name = match.group("template_name") or default_template_name
        yaml_text = match.group("yaml")

        if template_name not in templates:
            raise ValueError(f"Unknown template: {template_name}")

        block_data = yaml.safe_load(yaml_text)
        if not isinstance(block_data, dict):
            raise ValueError("Embedded YAML block must parse to a mapping.")

        rendered = render_template_block(
            block_data=block_data,
            template_spec=templates[template_name],
            jinja_env=jinja_env,
        )

        return "\n".join(
            indent + line if line.strip() else line
            for line in rendered.splitlines()
        )

    return YAML_BLOCK_PATTERN.sub(repl, source_text)


def render_yphs_to_phs(
    source_text: str,
    template_data: dict[str, Any],
    default_template_name: str = "default",
) -> str:
    """
    Public API: render YPHS-style mixed text into pure Phenoscript text.

    Parameters
    ----------
    source_text
        Input text containing mixed Phenoscript and marked YAML blocks.
    template_data
        Parsed template YAML containing a top-level 'templates' mapping.
    default_template_name
        Template name to use when #>>>YAML has no explicit template suffix.

    Returns
    -------
    str
        Rendered Phenoscript text.
    """
    templates = template_data.get("templates")
    if not isinstance(templates, dict):
        raise ValueError("Template data must contain a top-level 'templates' mapping.")

    return replace_yaml_blocks(
        source_text=source_text,
        templates=templates,
        default_template_name=default_template_name,
    )


def render_yphs_file(
    input_path: str | Path,
    template_path: str | Path,
    output_path: str | Path | None = None,
    default_template_name: str = "default",
) -> str:
    """
    Read a mixed YPHS file, render it, and optionally write output to disk.

    Returns the rendered text.
    """
    input_path = Path(input_path)
    template_path = Path(template_path)

    source_text = input_path.read_text(encoding="utf-8")
    template_data = load_yaml_file(template_path)

    output_text = render_yphs_to_phs(
        source_text=source_text,
        template_data=template_data,
        default_template_name=default_template_name,
    )

    if output_path is not None:
        output_path = Path(output_path)
        output_path.write_text(output_text, encoding="utf-8")

    return output_text