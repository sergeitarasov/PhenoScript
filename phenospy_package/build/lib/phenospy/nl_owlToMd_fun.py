from colorama import Fore, Style
from colorama import init as colorama_init
colorama_init()
from phenospy.owl_owlready_config import *
import re

# -----------------------------------------
# Make NL Graph for Md rendering from OWL: high-level wrapper
# -----------------------------------------
def owlToNLgraph(owl_file):
    # -----------------------------------------
    # Arguments
    # -----------------------------------------
    # set_log_level(0)
    print(f"{Fore.BLUE}Reading OWL:{Style.RESET_ALL}", owl_file)
    onto = get_ontology(owl_file).load(reload_if_newer=True, reload=True)
    # -----------------------------------------
    # Namespaces
    # -----------------------------------------
    obo = onto.get_namespace("http://purl.obolibrary.org/obo/")
    phs_ns = onto.get_namespace('https://github.com/sergeitarasov/PhenoScript/')
    import phenospy.nl_fun
    # -----------------------------------------
    # Make NL graph 
    # -----------------------------------------
    phenospy.nl_fun.makeNLGraph_basic(onto)
    return onto


def substitute_unwanted_combinations(string):
    modified_string = string.replace(" ,", ",")
    modified_string = modified_string.replace(" :", ":")
    return modified_string

# finds lines that belong to metadata and placces them first
def find_and_move_lines(huge_string):
    # pattern = r'\)\s\['
    pattern = '^- [^\]]+\]\([^\)]+\) [^\]]+\]\([^\)]+\)'
    #lines = huge_string.split('\n')
    lines=re.split(r'\n(?!\t)', huge_string)
    matched_lines = []

    for line in lines:
        if re.search(pattern, line):
            matched_lines.append(line)

    modified_string = '\n'.join(matched_lines) + '\n' + '---' + '\n'.join(line for line in lines if line not in matched_lines)

    return modified_string


# Checks if there any URLS coming from quoted nodes that are not hyperlinked. Next, it hyperlinks them.
# html_output = convert_text_urls_to_links(markdown_text)
# print(html_output)
def convert_text_urls_to_links(markdown_text):
    # Define a regular expression pattern to match URLs that are not already in [link text](URL) format
    url_pattern = r'https?://[^\s()]+(?![^\s]*\))'
    # Find all URLs in the Markdown text that are not in [link text](URL) format
    urls_to_convert = re.findall(url_pattern, markdown_text)
    # Iterate through the found URLs and convert them to clickable hyperlinks
    for url in urls_to_convert:
        #print(url)
        markdown_text = re.sub(re.escape(url), f'[{url}]({url})', markdown_text)
    return markdown_text

# -----------------------------------------
# Make NL desciptions in Md format
# -----------------------------------------
# ind0 = onto.search(label = 'org_Grebennikovius_basilewskyi')[0]
def NLgraphToMarkdown(onto, ind0, file_save=None, verbose=False):
    
    print(f"{Fore.BLUE}Converting NL graph to Markdown...{Style.RESET_ALL}")
    global visited_nodes, visited_triples
    visited_nodes=set()
    visited_triples=list()
    #
    import phenospy.nl_fun
    md = phenospy.nl_fun.traverseGraphForNL(onto, ind0, tabs='\t', tab_char='\t', visited_nodes=set())
    # print(md)
    md_out = md.replace("\t [", " [")
    md_out = md_out.replace("\t [", "\t- [")
    md_out = md_out.replace("\n [", "\n- [")
    # remove unwanted combbinations of characters
    md_out = substitute_unwanted_combinations(md_out)
    # finds lines that belong to metadata and placces them first
    md_out = find_and_move_lines(md_out)
    # hyperlink unhyperlinked URL
    md_out = convert_text_urls_to_links(md_out)
    # Add species name as comment
    header = '<!-- ' + ind0.label.first() + ' -->\n'
    md_out = header + md_out
    #print(md_out)
    #
    visited_nodes=set()
    phenospy.nl_fun.visited_triples=list()

    
    if file_save is not None:
        print(f"{Fore.BLUE}Saving Markdown to:{Style.RESET_ALL}", file_save)
        fl = open(file_save, "w+")
        fl.writelines(md_out)
        fl.close()
    print(f"{Fore.GREEN}Done!{Style.RESET_ALL}")
    if verbose==True:
        return md_out