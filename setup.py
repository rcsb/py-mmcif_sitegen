# File: setup.py
# Date: 26-Mar-2020
#
# Update:
#
import re
from setuptools import setup, find_packages


packages = []
thisPackage = "mmcif.sitegen"


with open("mmcif/sitegen/dictionary/__init__.py", "r") as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError("Cannot find version information")

setup(
    name=thisPackage,
    version=version,
    description="mmCIF Dictionary Site Generator",
    long_description="See:  README.md",
    author="John Westbrook",
    author_email="john.westbrook@rcsb.org",
    url="http://mmcif.wwpdb.org",
    #
    license="Apache 2.0",
    classifiers=(
        "Development Status :: 3 - Alpha",
        # 'Development Status :: 5 - Production/Stable',
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ),
    entry_points={
        "console_scripts": [
            "site_generator_cli=mmcif.sitegen.wf.SiteGeneratorExec:main",
        ]
    },
    #
    install_requires=["mmcif >= 0.57", "rcsb.utils.io >= 0.95"],
    packages=find_packages(exclude=["mmcif.sitegen.tests", "tests.*"]),
    package_data={
        # If any package contains *.md or *.rst ...  files, include them:
        "": ["*.md", "*.rst", "*.txt"],
    },
    #
    test_suite="mmcif.sitegen.tests",
    tests_require=["tox"],
    #
    # Not configured ...
    extras_require={
        "dev": ["check-manifest"],
        "test": ["coverage"],
    },
    # Added for
    # command_options={"build_sphinx": {"project": ("setup.py", thisPackage), "version": ("setup.py", version), "release": ("setup.py", version)}},
    zip_safe=False,
)
