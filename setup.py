"""Setup for the simple package."""

import setuptools

setuptools.setup(
    name="simple",
    version="0.0.0",
    author="Jonathan Winn",
    author_email="jonathan.winn@metoffice.com",
    description="Training example package",
    url="https://github.com/cma-open/simple",
    # find and install all packages
    package_dir={"": "src"},
    # Legacy / Maintenance note:
    # As the package dir is  specified, then don't need to also exclude the tests here
    # However retained as a failsafe in case future tests are added in the main package
    packages=setuptools.find_packages(where="src", exclude=["*tests.*", "*tests"]),
    license="BSD",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    # Set minimum python version to allow installation
    python_requires=">=3.10",
    # Considers all non .py files found inside the package directory as data files
    include_package_data=True,
    # Register command line scripts from the relevant package module
    # These are added as command line options once the system is installed
    entry_points={
        # Name the tool, link to the package function
        "console_scripts": [
            # Name the simple analysis command
            "cli-simple=" "simple.cli:cli_entry_point",
            "confirm-config=" "simple.config.reader:main",
        ]
    },
)

# Developer and review notes
# This includes data files WITHIN the src package
# Check and review use of other methods if files from repo root are also needed
# e.g. MANIFEST.in
