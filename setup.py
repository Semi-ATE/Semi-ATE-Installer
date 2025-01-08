from setuptools import find_packages, setup
from pathlib import Path

requirements_path = Path(Path(__file__).parents[0], 'requirements/run.txt')
print(f">>>>> requiremets_path ={requirements_path}")

with requirements_path.open('r') as f:
    install_requires = list(f)


setup(
    name='semi-ate-installer',
    version='0.0.0',
    description='Semi ATE Installer package for ATE Projects',
    long_description='',
    long_description_content_type='text/markdown',
    author="The Semi-ATE Project Contributors",
    author_email="ate.organization@gmail.com",
    license="GPL-2.0-only",
    keywords="Semiconductor ATE Automatic Test Equipment Spyder Plugin",
    platforms=["Windows", "Linux", "Mac OS-X"],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
    ],
    install_requires=install_requires,
    entry_points={
        'console_scripts': ['ate-installer=semi_ate_installer.cli:main']
    },
)
