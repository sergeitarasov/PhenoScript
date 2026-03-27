
import os
import requests
import yaml
import re

from colorama import Fore, Style
from colorama import init as colorama_init

colorama_init()

#----------- Download Ontologies from YAML file
def download_ontologies_from_yaml(yaml_file, save_dir):
    # -----------------------------------------
    # Read configuration yaml
    # -----------------------------------------
    print(f"{Fore.BLUE}Reading yaml file: {Style.RESET_ALL}{yaml_file}")
    with open(yaml_file, 'r') as f_yaml:
        phs_yaml = yaml.safe_load(f_yaml)
    # print(phs_yaml)
    print(f"{Fore.GREEN}Good! File is read!{Style.RESET_ALL}")

    # Create a directory to store downloaded ontologies
    os.makedirs(save_dir, exist_ok=True)
    print(f"{Fore.BLUE}Downloading ontologies to: {Style.RESET_ALL}{save_dir}")

    # Iterate over the ontologies and download them
    for ontology_url in phs_yaml['importOntologies']:
        # Get the filename from the URL
        filename = os.path.basename(ontology_url)
        file_path = os.path.join(save_dir, filename)

        # Download the ontology
        response = requests.get(ontology_url)
        if response.status_code == 200:
            with open(file_path, 'wb') as ontology_file:
                ontology_file.write(response.content)
            print(f"{Fore.BLUE}Downloaded: {filename}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Failed to download: {filename}{Style.RESET_ALL}")
    
    print(f"{Fore.GREEN}All ontologies downloaded.{Style.RESET_ALL}")



#----------- Find available version of Phenoscript extensions: Mac only
# get all full paths to phenoscript extensions
def find_phenoscript_extensions():
    vscode_extensions_dir = os.path.expanduser("~/.vscode/extensions")
    phenoscript_folders = []

    # List all folders in the ~/.vscode/extensions directory
    extension_folders = os.listdir(vscode_extensions_dir)

    # Filter folders that contain "tarasov-lab.phenoscript"
    for folder in extension_folders:
        if "tarasov-lab.phenoscript" in folder:
            phenoscript_folders.append(folder)

    # Sort folders by version number (assuming format '0.0.XX')
    phenoscript_folders.sort(reverse=True, key=lambda folder: [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', folder)])

    # Create full paths to the folders
    phenoscript_paths = [os.path.join(vscode_extensions_dir, folder) for folder in phenoscript_folders]

    return phenoscript_paths

# print full paths to phenoscript extensions
def print_phenoscript_extensions():
    phenoscript_paths=find_phenoscript_extensions()
    if len(phenoscript_paths):
        latest = phenoscript_paths[0]
        others = phenoscript_paths[1:]
        others = '\n'.join(others)
        print(f"{Fore.GREEN}The latest version:\n{Style.RESET_ALL}{latest}")
        print(f"{Fore.BLUE}Other versions:\n{Style.RESET_ALL}{others}")
    else:
        print(f"{Fore.RED}No extension found. This function currently works on Mac only.{Style.RESET_ALL}")


def save_to_file(file_content, output_file):
    with open(output_file, 'w', encoding='utf-8') as fl:
        fl.write(file_content)