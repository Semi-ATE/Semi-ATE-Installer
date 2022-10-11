from setuptools import setup

from setuptools.config import read_configuration
conf_dict = read_configuration("setup.cfg")
PKG_NAME = conf_dict['metadata']['name']

if __name__ == "__main__":
    setup(
        use_scm_version={"write_to": f"{PKG_NAME}/_version.py"}
    )
