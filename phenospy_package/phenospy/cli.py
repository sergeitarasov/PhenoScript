from .phs_mainConvert import phsToOWL
from .utils import download_ontologies_from_yaml, print_phenoscript_extensions
from .snips_makeFromYaml import make_vscodeSnips
import argparse
import os

import warnings
# Set the warning filter to suppress all warnings
warnings.filterwarnings("ignore")


def owl2md(args):
    # Implement logic for command 1
    print(f"Executing command 1 with arguments: {args.arg1}")

def phs2owl(args):
    print("Executing phs2owl ... ")
    # Split the path into directory and filename
    directory, filename = os.path.split(args.output_base)
    # Check if the output directory exists and create it if necessary
    if not os.path.exists(directory):
        os.makedirs(directory)
    #
    phs_file    = args.phs_file
    yaml_file   = 'phs-config.yaml'
    save_dir    = directory
    save_pref   = filename
    phsToOWL(phs_file, yaml_file, save_dir, save_pref)


# -------- Main
def main():
    parser = argparse.ArgumentParser(description="Phenospy Command-Line Tools")
    
    subparsers = parser.add_subparsers(title="commands", dest="command")

    # get phenoscript extension paths and versions
    parser_commandPath = subparsers.add_parser("get-vsc", help="Get Phenoscript plugin versions for VS Code. For Mac only.")
    parser_commandPath.epilog = "Examples:\n" \
        "phenospy get-vsc\n"
    
    # make snippets
    parser_commandSnip = subparsers.add_parser("make-snips", help="Make VS Code snippets.")
    parser_commandSnip.add_argument("yaml_file", help="Input yaml file.")
    parser_commandSnip.epilog = "Examples:\n" \
        "phenospy make-snips 'phs-config.yaml'\n"

    # phs2owl
    parser_command1 = subparsers.add_parser("phs2owl", help="Convert PHS file to OWL.")
    parser_command1.add_argument("phs_file", help="Input phs file.")
    parser_command1.add_argument("output_base", help="Base name for output files; two output files will be produced (xml and owl).")
    #   Provide examples for "command1" usage
    parser_command1.epilog = "Examples:\n" \
        "phenospy phs2owl 'input.phs' 'file_out'\n" \
        "phenospy phs2owl 'input.phs' 'output/file_out"
    
    # owl2md
    parser_command2 = subparsers.add_parser("owl2md", help="Convert OWL file to Markdown.")
    parser_command2.add_argument("arg1", help="Argument for command 1.")

    # fetch-ontos
    parser_command3 = subparsers.add_parser("fetch-ontos", help="Download ontologies from phs-config.yaml file.")
    parser_command3.add_argument("yaml_file", help="Input yaml file.")
    parser_command3.add_argument("output_dir", help="Folder to save ontologies.")
    parser_command1.epilog = "Examples:\n" \
        "phenospy fetch-ontos 'phs-config.yaml' '/source_ontologies'\n"
    
    args = parser.parse_args()
    if args.command == "owl2md":
        owl2md(args)
    elif args.command == "phs2owl":
        phs2owl(args)
    elif args.command == "fetch-ontos":
        download_ontologies_from_yaml(args.yaml_file, args.output_dir)
    elif args.command == "make-snips":
        make_vscodeSnips(args.yaml_file)
    elif args.command == "get-vsc":
        print_phenoscript_extensions()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
