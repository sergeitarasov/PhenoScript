1. To install owlready:
conda install -c conda-forge owlready2=2.4.2
or
pip install owlready2



# PhenoScript
 The computer language for describing species and phenotypes 

## Requirements

* Python >=3.6
* R>=3.6.2
* [ROBOT](http://robot.obolibrary.org)
* [Atom](https://atom.io)
* macOS (runs on Linux and Windows but no installation instruciton is yet provided. You can try intalling it yourself)

## Install
1. First install [Atom](https://atom.io) and [PhenoScript Atom package](https://github.com/sergeitarasov/phs-syntax) to have syntax highlight. The instructions is in the last link.
1. Install [ROBOT](http://robot.obolibrary.org) and update your systme PATH (see intruction on ROBOT's website) so that the ROBOT is executable from the command line in any directory
2. In Terminal `cd`  to  `PhenosScript/src` and run `python setup.py`to install necessary python modules.
3. If all goes seccessfull then the installation is complete.
4. Put two files `phs.py` and `snips.py` from `PhenosScript` folder into your systme PATH (to make them executable from the command line in any directory).
5. In `PhenosScript/phs_Global_Args.txt` provide the path to the Atom directory  where `snippets.cson` file is located (click on `Atom -> Snippets...`to see the file and its directory) via `PATH_TO_ATOM =`. Also provide an IRI for onotlogy instances via `INSTANCE_IRI=`.

## Quick start guide



### Install the necessary packages
```{r}
install.packages("ontoFAST")
install.packages("igraph")
library("ontoFAST")
```
