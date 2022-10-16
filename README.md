# Semi-ATE-Installer



[![GitHub](https://img.shields.io/github/license/Semi-ATE/Semi-ATE-installer?color=black)](https://github.com/Semi-ATE/Semi-ATE-Installer/blob/master/LICENSE)
[![Conda](https://img.shields.io/conda/pn/conda-forge/starz?color=black)](https://www.lifewire.com/what-is-noarch-package-2193808)
[![Supported Python versions](https://img.shields.io/badge/python-%3E%3D3.8-black)](https://www.python.org/downloads/)
[![CI-CD](https://github.com/Semi-ATE/Semi-ATE-Installer/workflows/python-publish/badge.svg)](https://github.com/Semi-ATE/Semi-ATE-Installer/actions/workflows/python-publish.yml?query=workflow%3ACD)

[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/Semi-ATE/Semi-ATE-Installer?color=blue&label=GitHub&sort=semver)](https://github.com/Semi-ATE/Semi-ATE-Installer/releases/latest)
[![GitHub commits since latest release (by date)](https://img.shields.io/github/commits-since/Semi-ATE/Semi-ATE-Installer/latest)](https://github.com/Semi-ATE/Semi-ATE-Installer)
[![GitHub issues](https://img.shields.io/github/issues/Semi-ATE/Semi-ATE-Installer)](https://github.com/Semi-ATE/Semi-ATE-Installer/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/Semi-ATE/Semi-ATE-Installer)](https://github.com/Semi-ATE/Semi-ATE-Installer/pulls)

[![Conda (channel only)](https://img.shields.io/conda/vn/conda-forge/Semi-ATE-installer?color=blue&label=conda-forge)](https://anaconda.org/conda-forge/semi-ate-installer)  [![conda-forge feedstock](https://img.shields.io/github/issues-pr/conda-forge/Semi-ATE-Installer-feedstock?label=feedstock)](https://github.com/conda-forge/semi-ate-installer-feedstock)

The installation package that will install the correct Semi-ATE packages depending on the use-case.

## Installation

Make sure that conda is installed. The preferred way is to install [maxiconda](https://github.com/Semi-ATE/maxiconda) that brings `conda` to your system and also generates a small environment called `base`. It is **IMPERATIVE** that this package is installed in the `base` environment. 

1. `conda activate base`
2. `mamba install Semi-ATE-Installer`
3. Execute `ate-installer` and follow the installer.
