# Semi-ATE-Installer

[![GitHub](https://img.shields.io/github/license/Semi-ATE/Semi-ATE-installer?color=black)](https://github.com/Semi-ATE/Semi-ATE-Installer/blob/master/LICENSE)
[![Conda](https://img.shields.io/conda/pn/conda-forge/starz?color=black)](https://www.lifewire.com/what-is-noarch-package-2193808)
[![Supported Python versions](https://img.shields.io/badge/python-%3E%3D3.8-black)](https://www.python.org/downloads/)

[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/Semi-ATE/Semi-ATE-Installer?color=blue&label=GitHub&sort=semver)](https://github.com/Semi-ATE/Semi-ATE-Installer/releases/latest)
[![GitHub commits since latest release (by date)](https://img.shields.io/github/commits-since/Semi-ATE/Semi-ATE-Installer/latest)](https://github.com/Semi-ATE/Semi-ATE-Installer)
[![GitHub issues](https://img.shields.io/github/issues/Semi-ATE/Semi-ATE-Installer)](https://github.com/Semi-ATE/Semi-ATE-Installer/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/Semi-ATE/Semi-ATE-Installer)](https://github.com/Semi-ATE/Semi-ATE-Installer/pulls)

[![Conda (channel only)](https://img.shields.io/conda/vn/conda-forge/Semi-ATE-installer?color=blue&label=conda-forge)](https://anaconda.org/conda-forge/semi-ate-installer)  [![conda-forge feedstock](https://img.shields.io/github/issues-pr/conda-forge/Semi-ATE-Installer-feedstock?label=feedstock)](https://github.com/conda-forge/semi-ate-installer-feedstock)

The installation package that will install the correct [Semi-ATE packages](https://github.com/Semi-ATE/Semi-ATE) depending on the use-case.

## Installation

Make sure that conda is installed via [maxiconda](https://www.maxiconda.org/). This brings `conda` **and** `mamba` to your system. It is **IMPERATIVE** that this package is installed in the `base` environment! 

1. Go to the base environment by executing `conda activate base`
2. Install the Semi-ATE Installer by executing `mamba install Semi-ATE-Installer`
3. Install Semi-ATE in an environment by executing `ate-installer`, select the environment and follow the installer.
