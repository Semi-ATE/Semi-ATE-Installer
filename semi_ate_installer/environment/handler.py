from enum import IntEnum
import sys
from typing import List, Tuple
import re
from conda.cli.python_api import Commands, run_command
from mamba.utils import print_activate
from semi_ate_installer.channel.repository import Repository

from semi_ate_installer.utils.packages import RequiredPackage, SemiAtePackage, PackageInfo
from semi_ate_installer.utils.profiles import Profiles


class HandlerType(IntEnum):
    Mamba = 0
    Conda = 1


class EnvironmentHandler:
    @staticmethod
    def get_installed_packages(env_name: str) -> Tuple[List[str], List[str]]:
        result = run_command(Commands.LIST, '-n', env_name, use_exception_handler=False)
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

        all_packages = [PackageInfo(e.split('*')[0], e.split('*')[1]) for e in temp]

        semi_ate_packages = list(filter(lambda p: p.name in map(lambda n: n(), list(SemiAtePackage)), all_packages))
        required_packages = list(filter(lambda p: p.name in map(lambda n: n(), list(RequiredPackage)), all_packages))

        return semi_ate_packages, required_packages

    @staticmethod
    def install_packages(handler_type: HandlerType, env_name: str, packages: List[str]) -> None:
        if handler_type == HandlerType.Mamba:
            MambaEnvHandler.create_env(env_name, packages)
        else:
            CondaEnvHandler.create_env(env_name, packages)

    @staticmethod
    def get_available_environments() -> List[str]:
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

        return [path.split('*')[0] for path in temp.split(';')]

    @staticmethod
    def create_env(handler_type: HandlerType, env_name: str, packages: List[str] = []):
        if handler_type == HandlerType.Mamba:
            MambaEnvHandler.create_env(env_name, packages)
        else:
            CondaEnvHandler.create_env(env_name, packages)

    @staticmethod
    def get_packages(profile: str) -> List[str]:
        return {
            Profiles.TestProgramDeveloper: PackageHandler.get_test_program_developer_packages
        }[profile]()

    @staticmethod
    def print_activate(env_name: str):
        print_activate(env_name)

    @staticmethod
    def are_updates_available(env_name: str) -> bool:
        available_packages = PackageHandler.get_available_packages_version(SemiAtePackage.get_fields())
        print(available_packages)
        return False


class MambaEnvHandler:
    @staticmethod
    def create_env(env_name: str, packages: List[str] = []):
        from mamba.api import create
        create(env_name, specs=tuple(packages), channels=('conda-forge', ))

    @staticmethod
    def install_packages(env_name: str, packages: List[str]):
        from mamba.api import install
        install(env_name, specs=tuple(packages), channels=('conda-forge', ))


class CondaEnvHandler:
    @staticmethod
    def create_env(env_name: str, packages: List[str] =[]):
        from conda.cli.python_api import Commands, run_command
        run_command(Commands.CREATE, '-n', env_name, 'python=3', *packages, '-y', use_exception_handler=False, stdout=sys.stdout)

    @staticmethod
    def install_packages(env_name: str, packages: List[str]):
        from conda.cli.python_api import Commands, run_command
        run_command(Commands.INSTALL, '-n', env_name, *packages, '-y', use_exception_handler=False, stdout=sys.stdout)


class PackageHandler:
    @staticmethod
    def get_test_program_developer_packages() -> List[str]:
        packages = SemiAtePackage.get_fields()
        packages.extend(RequiredPackage.get_fields())
        return packages

    @staticmethod
    def get_available_packages_version(packages: List[str]) -> List[PackageInfo]:
        joined_packages = '^('
        joined_packages += '|'.join([package for package in packages])
        joined_packages += ')$'
        print(Repository.get_available_versions(joined_packages))
        # TODO: compare with those whom are installed

    @staticmethod
    def get_installed_packages(env_name: str) -> List[PackageInfo]:
        pass
