# mmCIF Dictionary Site Generator

[![Build Status](https://dev.azure.com/rcsb/RCSB%20PDB%20Python%20Projects/_apis/build/status/rcsb.py-mmcif_sitegen?branchName=dev-20201227)](https://dev.azure.com/rcsb/RCSB%20PDB%20Python%20Projects/_build/latest?definitionId=30&branchName=dev-20201227)

## Introduction

This module contains a collection of utilities to generate HTML and image
content for the [mmCIF Resource Site](mmcif.wwpdb.org)

## Installation

Install from PyPi using:

```bash
pip install mmcif.sitegen
```

To install from source, download the library source software from the project repository:

```bash

git clone  https://github.com/rcsb/py-mmcif_sitegen.git

cd py-mmcif_sitegen
pip install -e .

```

Optionally, run the test suite, using:

```bash

python setup.py test

or

tox

```

A command line entry point with the following options is provided to generate html and images:

```bash
 site_generator_cli --help

usage: SiteGeneratorExec.py [-h] [--web_gen_path WEB_GEN_PATH] [--web_file_assets_path WEB_FILE_ASSETS_PATH] [--html] [--images] [--test_mode_flag]

optional arguments:
  -h, --help            show this help message and exit
  --web_gen_path WEB_GEN_PATH
                        Top path to website generated content
  --web_file_assets_path WEB_FILE_ASSETS_PATH
                        Top path for website source file assests
  --html                Generate HTML content
  --images              Generate image content
  --test_mode_flag      Test mode flag (default=False)

```
