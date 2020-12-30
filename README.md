## mmCIF Dictionary Site Generator

### Introduction

This module contains a collection of utility classes used to generate
marked-u content for the [mmCIF Resource Site](mmcif.wwpdb.org)

### Installation

Download the library source software from the project repository:

```bash

git clone  https://github.com/rcsb/py-mmcif_sitegen.git

```
This is preliminary port which continues to use test examples to
to generate site HTML and image content.   This is working
with new Python framework (Python 3.5 - 3.9) but
is lacking a proper CLI to control an configure general operations.

Optionally, run test suite (Python versions 2.7 or 3.6) which generates a site
in addition to running other tests, using:

```bash
python setup.py test

or

tox

```
