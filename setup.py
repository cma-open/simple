"""Setup for the simple package."""

import setuptools

setuptools.setup(
    name="simple",
    version="2023.01",
    author="Jonathan Winn",
    author_email="jonathan.winn@metoffice.com",
    description="Training example package",
    url="https://github.com/cma-open/simple",
    # Set package dir to identify package(s) to install, find within src dir
    packages=setuptools.find_packages(where="src", exclude=["*tests.*", "*tests"]),
    package_dir={
        "": "src",  # install system package from root, then src directory
    },
    license="BSD",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    # Set minimum python version to allow installation
    python_requires=">=3.10",
    # Considers all non .py files found inside the package directory as data files
    # MUST also be specified in the MANIFEST.in file
    include_package_data=True,
    # Register command line scripts from the relevant package module
    # These are added as command line options once the system is installed
    entry_points={
        # Name the command tools, link to the package functions
        "console_scripts": [
            # Name cli-simple command (uses argparse)
            "cli-simple=" "simple.cli:cli_entry_point",
            # Name confirm-config command
            "confirm-config=simple.config.reader:main",
            # Name create-data command (cf with options)
            "create-data=" "simple.netcdf.data:main",
            # Name create-data-options command (uses argparse)
            "create-data-options=" "simple.cli:cli_data",
            # Name clean command
            "clean=" "simple.io.io:main",
            # Name demo command
            "demo=" "simple.logging.log",
        ]
    },
    # TODO note deprecated - monitor, review, move later to use pyproject.toml
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
)

# TODO - check issues below
#####################################################################
# Architecture / design / code review notes (training use)
#####################################################################
# This includes data files WITHIN the src package
# PyPA recommends that any data files you wish to be accessible
# at run time be included inside the package.
# Check and review use of other methods if files from repo root
# are also needed
# Note - there are other methods to specify data files from version
# control and using package_data option.
# For now use of MANIFEST.in is acceptable.
# Review in Q1 2024. See #35
# Check conversion and use of pyproject.toml
# - esp editable vs user install
# Refs
# https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/
# https://setuptools.pypa.io/en/latest/userguide/datafiles.html#subdirectory-for-data-files
# https://packaging.python.org/en/latest/guides/using-manifest-in/
# https://docs.python.org/3/library/importlib.resources.html#module-importlib.resources
