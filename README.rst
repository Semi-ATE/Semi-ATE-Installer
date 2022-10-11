# Semi-ATE-Installer

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
