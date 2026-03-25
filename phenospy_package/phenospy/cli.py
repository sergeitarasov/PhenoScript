from .phs_mainConvert import phsToOWL
from .utils import download_ontologies_from_yaml, print_phenoscript_extensions, save_to_file
from .snips_makeFromYaml import make_vscodeSnips, make_mdSnips
from .nl_owlToMd_fun import owlToNLgraph, NLgraphToMarkdown
from .snips_fun import get_phenospyPath
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
    print("Executing phs2owl ... ")
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
        keep_raw=args.keep_raw
    )




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
        help="Convert PHS file to OWL.",
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
        help="Base name for output files; tree output files might be produced (xml, _raw.owl, owl)."
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
        help="Keep the intermediate raw OWL file (_raw.owl). Default: deleted."
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
    # owl2text
    # -----------------------------------------
    # parser_command2 = subparsers.add_parser("owl2text", help="Convert OWL file to Markdown or HTML.")
    # parser_command2.add_argument("-f", "--format", choices=["md", "html"], help="Output format: Markdown or HTML.")
    # parser_command2.add_argument("-s", "--search", help="OTU label search pattern.")
    # parser_command2.add_argument("-o", "--owl_file", help="Input OWL file.")
    # parser_command2.add_argument("-d", "--save_dir", help="Output directory.")
    # parser_command2.epilog = "Examples:\n" \
    #     "phenospy owl2text -f 'html' -s 'org_*' -o grebennikovius.owl -d NL\n"

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
    
    args = parser.parse_args()
    if args.command == "owl2text":
        owl2text(args)
    elif args.command == "phs2owl":
        phs2owl(args)
    elif args.command == "fetch-ontos":
        download_ontologies_from_yaml(args.yaml_file, args.output_dir)
    elif args.command == "make-snips":
        make_vscodeSnips(args.yaml_file)
    elif args.command == "make-md":
        make_mdSnips(args.yaml_file)
    elif args.command == "get-vsc":
        print_phenoscript_extensions()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
