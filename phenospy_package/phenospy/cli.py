from phenospy.phs_mainConvert import phsToOWL
from phenospy.utils import download_ontologies_from_yaml, print_phenoscript_extensions, save_to_file
from phenospy.snips_makeFromYaml import make_vscodeSnips, make_mdSnips
from phenospy.nl_owlToMd_fun import owlToNLgraph, NLgraphToMarkdown
from phenospy.snips_fun import get_phenospyPath
from phenospy.yphs import render_yphs_file
from phenospy.gbif_enrich import gbif_enrich_cli

import argparse
import os
import warnings
import rdflib  
# Set the warning filter to suppress all warnings
warnings.filterwarnings("ignore")
import markdown

from colorama import Fore, Style
from colorama import init as colorama_init
colorama_init()



#---------

def owl2text(args):
    print(f"{Fore.BLUE}Translating OWL to text...{Style.RESET_ALL}")
    # Split the directory of the input owl
    # it will be used to save intermediate _nl.owl
    owl_directory, owl_filename = os.path.split(args.owl_file)
    owl_name, owl_ext = os.path.splitext(owl_filename)
    # Handle case when no directory is provided (e.g., "file_out")
    if owl_directory == "":
        owl_directory = "."
    # Ensure output directory for html/md exists
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)
    #-----------------------
    # Load saved owl file with RDFLib
    #-----------------------
    print(f"{Fore.BLUE}Loading OWL into RDFLib...{Style.RESET_ALL}")
    g = rdflib.Graph()
    g.parse(args.owl_file, format="xml")
    print('DONE')
    #-----------------------
    # Apply SPARQL update
    #-----------------------
    print(f"{Fore.BLUE}Applying SPARQL update...{Style.RESET_ALL}")
    sparql_path = os.path.join(get_phenospyPath(), "package-data", "sparql-update", "update-owl-nl.ru")
    with open(sparql_path, "r", encoding="utf-8") as f:
        update_query = f.read()
    g.update(update_query)
    #-----------------------
    # Save updated graph
    #-----------------------
    updated_owl_nl = os.path.join(owl_directory, owl_name + '_nl.owl')
    g.serialize(destination=updated_owl_nl, format="xml")
    print(f"{Fore.GREEN}Done saving updated graph:{Style.RESET_ALL} {updated_owl_nl}")
    
    #-----------------------
    # Make NL Graph
    #-----------------------
    print(f"{Fore.BLUE}Making NL graph...{Style.RESET_ALL}")
    #onto = owlToNLgraph(args.owl_file)
    onto = owlToNLgraph(updated_owl_nl)
    # Save for debugging
    # graph_owl_nl = os.path.join(owl_directory, owl_name + '_graph-nl.owl')
    # onto.save(file = graph_owl_nl, format = "rdfxml")
    #-----
    # Get species/entry points for rendering
    entry_points = onto.search(label = args.search)
    print(f"{Fore.GREEN}Found OTUs: {Style.RESET_ALL}{len(entry_points)}")
    for point in entry_points:
        print(f"{Fore.BLUE}OTU: {Style.RESET_ALL}{point.label.first()}")
        md = NLgraphToMarkdown(onto, point, verbose = True)
        if args.format == "md":
            point_str = point.label.first()
            point_str = point_str.replace(" ", "_") + '.md'
            file_save = os.path.join(args.save_dir, point_str)
            save_to_file(md, file_save)
        elif args.format == 'html':
            html = markdown.markdown(md)
            point_str = point.label.first()
            point_str = point_str.replace(" ", "_") + '.html'
            file_save = os.path.join(args.save_dir, point_str)
            save_to_file(html, file_save)
    # -----------------------------------------
    # By defualt: delete updated_owl_nl
    # -----------------------------------------
    if not args.owl_nl:
        if os.path.exists(updated_owl_nl):
            os.remove(updated_owl_nl)




def phs2owl(args):
    print(f"{Fore.BLUE}Executing phs2owl ...{Style.RESET_ALL}")
    # Split the path into directory and filename
    directory, filename = os.path.split(args.output_base)
    # Handle case when no directory is provided (e.g., "file_out")
    if directory == "":
        directory = "."
    # Ensure output directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Inputs
    phs_file  = args.phs_file
    yaml_file = args.yaml_file
    save_dir  = directory
    save_pref = filename

    # Call main function
    phsToOWL(
        phs_file,
        yaml_file,
        save_dir,
        save_pref,
        keep_raw=args.keep_raw,
        enrich_gbif=args.enrich_gbif
    )


def yphs2owl(args):
    print(f"{Fore.BLUE}Executing yphs2owl ...{Style.RESET_ALL}")
    # Inputs
    # Remeber (for now) phs config-yaml and snippets.json must be in the same dir
    save_dir_owl, filename_owl = os.path.split(args.output_base)
    if save_dir_owl == "":
        save_dir_owl = "."
    os.makedirs(save_dir_owl, exist_ok=True)

    dir_yphs, file_yphs = os.path.split(args.yphs_file)
    name_yphs, ext_yphs = os.path.splitext(file_yphs)
    dir_intermediate_phs = dir_yphs
    if dir_intermediate_phs == "":
        dir_intermediate_phs = "."
    path_intermediate_phs = os.path.join(dir_intermediate_phs, f"{name_yphs}-yphs_inter.phs")
    #
    yaml_config_file = args.yaml_file
    # Built-in YAML template file for YPHS -> PHS rendering
    yaml_templates_file = os.path.join(get_phenospyPath(), "package-data", "yaml_temp", "phs_templates.yaml")
    # -----------------------------------------
    # yphs -> phs
    # -----------------------------------------
    render_yphs_file(
        input_path=args.yphs_file,
        template_path=yaml_templates_file,
        output_path=path_intermediate_phs,
    )
    # -----------------------------------------
    # phs -> OWL
    # -----------------------------------------
    phsToOWL(
        path_intermediate_phs,
        yaml_config_file,
        save_dir_owl,
        filename_owl,
        keep_raw=args.keep_raw,
        enrich_gbif=args.enrich_gbif
    )
    # -----------------------------------------
    # Cleanup intermediate .phs unless requested
    # -----------------------------------------
    if not args.keep_phs:
        if os.path.exists(path_intermediate_phs):
            os.remove(path_intermediate_phs)





# -----------------------------------------
# MAIN
# -----------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Phenospy Command-Line Tools")
    
    subparsers = parser.add_subparsers(title="commands", dest="command")

    # get phenoscript extension paths and versions
    parser_commandPath = subparsers.add_parser("get-vsc", help="Get Phenoscript plugin versions for VS Code. For Mac only.")
    parser_commandPath.epilog = "Examples:\n" \
        "phenospy get-vsc\n"
    
    # make snippets phs
    parser_commandSnip = subparsers.add_parser("make-snips", help="Make VS Code snippets.")
    parser_commandSnip.add_argument("yaml_file", help="Input yaml file.")
    parser_commandSnip.epilog = "Examples:\n" \
        "phenospy make-snips 'phs-config.yaml'\n"
    
    # make snippets Md
    parser_commandSnipMd = subparsers.add_parser("make-md", help="Make Markdown snippets.")
    parser_commandSnipMd.add_argument("yaml_file", help="Input yaml file.")
    parser_commandSnipMd.epilog = "Examples:\n" \
        "phenospy make-md 'phs-config.yaml'\n"


    # -----------------------------------------
    # phs2owl
    # -----------------------------------------
    parser_command1 = subparsers.add_parser(
        "phs2owl",
        help="Convert .phs file to OWL.",
        description=(
            "Convert a .phs file to OWL.\n\n"
            "Note:\n"
            "  This command requires three inputs:\n"
            "    1. .phs file (provided as argument)\n"
            "    2. YAML config file (provided or default: phs-config.yaml)\n"
            "    3. phs-snippets.json (path must be specified inside the YAML config)\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser_command1.add_argument(
        "phs_file",
        help="Input phs file."
    )
    parser_command1.add_argument(
        "output_base",
        help="Base name for output files; three output files might be produced (xml, _raw.owl, owl)."
    )
    # YAML config (short + long)
    parser_command1.add_argument(
        "-y", "--yaml",
        dest="yaml_file",
        metavar="FILE",
        default="phs-config.yaml",
        help="Path to YAML configuration file (default: phs-config.yaml)."
    )
    # keep raw (short + long)
    parser_command1.add_argument(
        "-k", "--keep-raw",
        action="store_true",
        help="Keep the intermediate raw OWL file (_raw.owl) generated before sparql unpdate. Default: deleted."
    )
    parser_command1.add_argument(
        "-g", "--enrich-gbif",
        action="store_true",
        help="Enrich Phenoscript file with GBIF taxonomy. Default: disabled."
    )
    # Examples
    parser_command1.epilog = (
        """Examples:
        phenospy phs2owl input.phs file_out
        phenospy phs2owl input.phs output/file_out
        phenospy phs2owl input.phs file_out --keep-raw
        phenospy phs2owl input.phs file_out -k
        phenospy phs2owl input.phs file_out --yaml config.yaml
        phenospy phs2owl input.phs file_out -y config.yaml
        phenospy phs2owl input.phs file_out -y configs/my.yaml -k
        """
    )

    # -----------------------------------------
    # yphs2owl
    # -----------------------------------------
    parser_yphs2owl = subparsers.add_parser(
    "yphs2owl",
    help="Convert a .yphs file to OWL.",
    description=(
        "Convert a .yphs file to OWL.\n\n"
        "Note:\n"
        "  This command requires four inputs:\n"
        "    1. .yphs file (provided as argument)\n"
        "    2. output_base (provided as argument)\n"
        "    3. YAML config file (provided or default: phs-config.yaml)\n"
        "    4. phs-snippets.json (path must be specified inside the YAML config)"
    ),
    formatter_class=argparse.RawTextHelpFormatter,)

    parser_yphs2owl.add_argument(
        "yphs_file",
        help="Input yphs file.",
    )

    parser_yphs2owl.add_argument(
        "output_base",
        help="Base name for output files; three output files might be produced (xml, _raw.owl, owl).",
    )

    parser_yphs2owl.add_argument(
        "-y", "--yaml",
        dest="yaml_file",
        default="phs-config.yaml",
        metavar="FILE",
        help="Path to YAML configuration file (default: phs-config.yaml).",
    )

    parser_yphs2owl.add_argument(
        "-k", "--keep-raw",
        action="store_true",
        help="Keep the intermediate raw OWL file (_raw.owl). Default: deleted.",
    )

    parser_yphs2owl.add_argument(
        "-P", "--keep-phs",
        action="store_true",
        help="Keep the intermediate phs file (-yphs_inter.phs). Default: deleted.",
    )

    #parser_yphs2owl.set_defaults(func=yphs2owl)
    parser_yphs2owl.epilog = (
        """Examples:
        phenospy yphs2owl input.phs file_out
        phenospy yphs2owl input.phs file_out -k -P
        """
    )
    parser_yphs2owl.add_argument(
        "-g", "--enrich-gbif",
        action="store_true",
        help="Enrich Phenoscript file with GBIF taxonomy. Default: disabled."
    )
    
    # -----------------------------------------
    # owl2text
    # -----------------------------------------
    parser_command2 = subparsers.add_parser(
    "owl2text",
    help="Convert an OWL file to Markdown or HTML.",
    description=(
        "Translate an OWL file into natural-language text and save the result "
        "as Markdown or HTML.\n\n"
        "The command first creates an intermediate '_nl.owl' file by applying "
        "a SPARQL update, then renders text for all matching OTU labels."
    ),
    formatter_class=argparse.RawTextHelpFormatter)

    parser_command2.add_argument(
        "-f", "--format",
        choices=["md", "html"],
        required=True,
        help="Output format: 'md' for Markdown or 'html' for HTML."
    )
    parser_command2.add_argument(
        "-s", "--search",
        required=True,
        metavar="PATTERN",
        help="OTU label search pattern, for example 'org_*'."
    )
    parser_command2.add_argument(
        "-o", "--owl-file",
        dest="owl_file",
        required=True,
        metavar="FILE",
        help="Input OWL file in RDF/XML format."
    )
    parser_command2.add_argument(
        "-d", "--save-dir",
        dest="save_dir",
        required=True,
        metavar="DIR",
        help="Directory where Markdown or HTML output files will be saved."
    )
    parser_command2.add_argument(
        "-k", "--keep-owl-nl",
        dest="owl_nl",
        action="store_true",
        help="Keep the intermediate '_nl.owl' file generated by sparql update. Default: deleted."
    )
    parser_command2.epilog = """Examples:
    phenospy owl2text -f html -s "org_*" -o grebennikovius.owl -d NL
    phenospy owl2text -f md   -s "org_*" -o output/specimen.owl -d text_out
    phenospy owl2text -f html -s "org_*" -o grebennikovius.owl -d NL --keep-owl-nl
    """

    # fetch-ontos
    parser_command3 = subparsers.add_parser("fetch-ontos", help="Download ontologies from phs-config.yaml file.")
    parser_command3.add_argument("yaml_file", help="Input yaml file.")
    parser_command3.add_argument("output_dir", help="Folder to save ontologies.")
    parser_command3.epilog = "Examples:\n" \
        "phenospy fetch-ontos 'phs-config.yaml' '/source_ontologies'\n"
    
    # -----------------------------------------
    # gbif enrcih taxonomy
    # -----------------------------------------
    parser_gbif_enrich = subparsers.add_parser(
        "gbif-enrich",
        help="Enrich a .phs file with taxonomy from GBIF.",
        description=(
            "Read a .phs file, find GBIF taxon identifiers in "
            ".dwc-Taxon_ID_taxonID lines, query GBIF, and insert "
            "missing taxonomy such as scientific name, genus, family, "
            "order, class, phylum, and kingdom."
        ),
        epilog="""
            Examples:
            phenospy gbif-enrich input.phs output_enriched.phs
            phenospy gbif-enrich input.phs output.phs --timeout 10
            phenospy gbif-enrich input.phs output.phs --no-blank-line
            """,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser_gbif_enrich.add_argument(
        "phs_file",
        help="Input .phs file.",
    )
    parser_gbif_enrich.add_argument(
        "output_file",
        help="Output enriched .phs file.",
    )
    parser_gbif_enrich.add_argument(
        "--timeout",
        type=int,
        default=20,
        help="HTTP timeout for GBIF requests in seconds (default: 20).",
    )
    parser_gbif_enrich.add_argument(
        "--no-blank-line",
        action="store_true",
        help="Do not insert a blank line after added taxonomy lines.",
    )
    #parser_gbif_enrich.set_defaults(func=gbif_enrich_cli)
    
    args = parser.parse_args()
    if args.command == "owl2text":
        owl2text(args)
    elif args.command == "phs2owl":
        phs2owl(args)
    elif args.command == "yphs2owl":
        yphs2owl(args)
    elif args.command == "fetch-ontos":
        download_ontologies_from_yaml(args.yaml_file, args.output_dir)
    elif args.command == "make-snips":
        make_vscodeSnips(args.yaml_file)
    elif args.command == "make-md":
        make_mdSnips(args.yaml_file)
    elif args.command == "get-vsc":
        print_phenoscript_extensions()
    elif args.command == "gbif-enrich":
        gbif_enrich_cli(args)
    else:
        parser.print_help()





if __name__ == "__main__":
    main()
