# Semi-ATE-Installer



[![GitHub](https://img.shields.io/github/license/Semi-ATE/Semi-ATE_installer?color=black)](https://github.com/Semi-ATE/Semi-ATE-Installer/blob/master/LICENSE.txt)
[![Conda](https://img.shields.io/conda/pn/conda-forge/starz?color=black)](https://www.lifewire.com/what-is-noarch-package-2193808)
[![Supported Python versions](https://img.shields.io/badge/python-%3E%3D3.8-black)](https://www.python.org/downloads/)
[![CI-CD](https://github.com/Semi-ATE/Semi-ATE/workflows/CI-CD/badge.svg)](https://github.com/Semi-ATE/Semi-ATE/actions/workflows/CICD.yml?query=workflow%3ACD)

[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/Semi-ATE/Semi-ATE?color=blue&label=GitHub&sort=semver)](https://github.com/Semi-ATE/Semi-ATE/releases/latest)
[![GitHub commits since latest release (by date)](https://img.shields.io/github/commits-since/Semi-ATE/Semi-ATE/latest)](https://github.com/Semi-ATE/Semi-ATE)
[![GitHub issues](https://img.shields.io/github/issues/Semi-ATE/Semi-ATE)](https://github.com/Semi-ATE/Semi-ATE/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/Semi-ATE/Semi-ATE)](https://github.com/Semi-ATE/Semi-ATE/pulls)

The installation package that will install the correct Semi-ATE packages depending on the use-case.

## Requirements

Make sure that conda ist installed. The preferred way is to install [maxiconda](https://github.com/Semi-ATE/maxiconda) that brings `conda` to your system and also generates a small environment called _base_.

## Installation

After checking out this repository perform the following steps in the root directory of the repository.

1. `conda activate base`
2. `python -m pip install .`

The above commands will install a command line tool called `ate-installer` that can be used to generate environments that contain every package from the [Semi-ATE](https://github.com/Semi-ATE/Semi-ATE) project that are needed to develop and run test programs.

**IMPORTANT** It is important to install and execute the ate-installer in the base environment.

## Future plans

* The installer will become part of maxiconda. This will make the manual installation of the ate-installer obsolete.


PR for feedstock : https://github.com/conda-forge/staged-recipes/pull/20724
