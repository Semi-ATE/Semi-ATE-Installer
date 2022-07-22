from numbers import Number
import sys
from typing import List
import re
from conda.cli.python_api import Commands, run_command
from utils.packages import RequiredPackage, SemiAtePackage, InstalledPackageInfo

class Environment:

    name: str
    path: str

    semi_ate_packages: List[InstalledPackageInfo]
    required_packages: List[InstalledPackageInfo]

    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path
        self.semi_ate_packages = []
        self.required_packages = []

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return (f'{self.name} ({self.path})')

    def get_installed_packages(self) -> None:
        result = run_command(Commands.LIST, '-n', f'{self.name}', use_exception_handler=False)
        # remove first three lines
        temp = re.sub(r'#.*\n', '', result[0])
        # replace spaces by *
        temp = re.sub(r'[^\S\n\t]+', '*', temp)
        # remove empty lines
        temp = re.sub(r'^[\s\t]*$\n', '', temp, flags=re.MULTILINE)
        # replace line end by :
        temp = re.sub(r'\n', ';', temp, flags=re.MULTILINE)
        # remove last 
        if temp[len(temp) - 1] == ';':
            temp = temp[:-1]

        temp = temp.split(';')

        all_packages = [InstalledPackageInfo(e.split('*')[0], e.split('*')[1]) for e in temp ]

        self.semi_ate_packages = list(filter(lambda p: p.name in map(lambda n: n(),list(SemiAtePackage)), all_packages))
        self.required_packages = list(filter(lambda p: p.name in map(lambda n: n(),list(RequiredPackage)), all_packages))
    
    def install_packages(self, packages: List[str]) -> None:
        run_command(Commands.INSTALL, '-n', f'{self.name}', *packages, '-y', use_exception_handler=False, stdout=sys.stdout)

    def uninstall_package(package: str) -> None:
        pass

class EnvironmentHandler:
    @staticmethod
    def get_available_environments() -> List[Environment]:

        environments = run_command(Commands.INFO, '--envs')
        # remove first two lines
        temp = environments[0].split("\n",2)[2]
        # replace * by space
        temp = temp.replace("*"," ")
        # replace spaces by ,
        temp = re.sub(r'[^\S\n\t]+', '*', temp)
        # remove empty lines
        temp = re.sub(r'^[\s\t]*$\n', '', temp, flags=re.MULTILINE)
        # replace line end by :
        temp = re.sub(r'\n', ';', temp, flags=re.MULTILINE)
        # remove last 
        if temp[len(temp) - 1] == ';':
            temp = temp[:-1]

        envs = temp.split(';')

        return [Environment(e.split('*')[0], e.split('*')[1]) for e in envs ]

