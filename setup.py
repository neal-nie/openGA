"""
openGA
"""
# Copyright (c) 2015-2021 Neal Nie. All rights reserved.

from pathlib import Path
from setuptools import find_packages, setup

PROJECT_PATH = Path(__file__).parent


with (PROJECT_PATH / "requirements.txt").open() as f:
    install_requires = [l.strip() for l in f.readlines()]


def _get_version():
    with PROJECT_PATH.joinpath("openGA", "version.py").open() as f:
        line = next(line for line in f if line.startswith("__version__"))

    version = line.partition("=")[2].strip()[1:-1]

    return version


def _get_long_description():
    description = PROJECT_PATH.joinpath("README.md").read_text(encoding="utf-8")

    return description



setup(
    name="openGA",
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=_get_version(),
    description="genetic algorithm framework",
    long_description=_get_long_description(),
    long_description_content_type=r"text/markdown",
    # The project's main homepage.
    url="https://github.com/neal-nie/openGA",
    # Author details
    author="Neal Nie",
    author_email="neal.nie@hotmail.com",
    # Choose your license
    license="LGPLv3+",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    # What does your project relate to?
    keywords="calibration adas automatic",
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(include=("openGA*",)),
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=install_requires
)
