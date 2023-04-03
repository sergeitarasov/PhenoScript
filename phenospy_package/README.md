![PyPI - Downloads](https://img.shields.io/pypi/dm/phenospy?color=blue&label=PyPI%20Downloads)

# Phenospy (= Phenoscript Python tools)

 <p align="left">
  <img src="https://raw.githubusercontent.com/sergeitarasov/PhenoScript/main/phenospy.png" width="300" title="Phenospy logo">
</p> 


[Phenospy](https://pypi.org/project/phenospy/) is a Python package that facilitates the automatic analysis and comparison of ontology-based (= semantic) descriptions of species and phenotypes. Phenospy works with descriptions written in [Phenoscript](https://github.com/sergeitarasov/vscode-phenoscript), a computer language designed for describing species (support for other semantic approaches is under development). 

The Phenoscript language allows rapid coding of morphological and ecological traits using an individual-based approach (ontology's A-box). You can efficiently code Phenoscript by using the [VS Code Phenoscript extension](https://marketplace.visualstudio.com/items?itemName=Tarasov-Lab.phenoscript) that provides syntax highlighting and snippet support. It can be installed from the Marketplace from within the VS Code. Its GitHub repository can be accessed [here](https://github.com/sergeitarasov/vscode-phenoscript). Afterward, Phenospy can be used to analyze and process the semantic descriptions.



## What can I do with Phenospy?

- Create snippets based on selected ontologies for writing semantic phenotypes with the VS Code Phenoscript extension.
- Convert the Phenoscript description into an OWL file.
- Convert the Phenoscript description into an annotated Natural Language description (Markdown format).
- Automatically compare species and phenotypes (under development).

## Requirements

* `Python >=3.0`

If you are a new user with Python 2 installed, you should uninstall it and install Python 3 instead. For more information, please refer to [this discussion](https://stackoverflow.com/questions/3819449/how-to-uninstall-python-2-7-on-a-mac-os-x-10-6-4).


## Install
Phenospy can be installed directly from the [PyPI repository](https://pypi.org/project/phenospy/) by running the following command in your terminal (macOS) or a command prompt (Windows):

```{bash}
pip install phenospy
```
### Troubleshooting
Pip is usually pre-installed with Python on macOS and Windows. However, if pip is not installed or you want to upgrade it to the latest version, you can follow these steps:

**For macOS:**
1. In your terminal type the following command to download the get-pip.py script:
```{bash}
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```
2. Type the following command to run the get-pip.py script and install pip:

```{bash}
sudo python get-pip.py
````
3. Verify that pip is installed by typing the following command:
```{bash}
pip --version
```

**For Windows:**

Open a command prompt by clicking on the "Start" menu, typing "cmd" into the search box, and selecting "Command Prompt" from the search results.

1. Type the following command to install pip:
```
py -m ensurepip --default-pip
```

2. Type the following command to upgrade pip to the latest version:
```
py -m pip install --upgrade pip
```







## Quick start guide

Coming soon.

### Let's create snippets

Coming soon.

### Let's convert Phenoscript into OWL

Coming soon.
