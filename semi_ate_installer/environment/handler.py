from enum import IntEnum
import sys
from typing import List, Tuple
import re
from conda.cli.python_api import Commands, run_command
from mamba.mamba import print_activate

from packaging import version

from semi_ate_installer.channel.repository import Repository
from semi_ate_installer.utils.packages import RequiredPackage, SemiAtePackage, PackageInfo
from semi_ate_installer.utils.profiles import Profiles


class HandlerType(IntEnum):
    Mamba = 0
    Conda = 1


class EnvironmentHandler:
    @staticmethod
    def get_installed_packages(env_name: str) -> List[PackageInfo]:
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

        all_packages = [PackageInfo(e.split('*')[0], version.parse(e.split('*')[1])) for e in temp]
        return all_packages

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
            Profiles.TestProgramDeveloper: EnvironmentHandler.get_test_program_developer_packages
        }[profile]()

    @staticmethod
    def print_activate(env_name: str):
        print_activate(env_name)

    @staticmethod
    def get_available_updates(env_name: str) -> List[Tuple[str, version.Version, version.Version]]:
        all_package_names = SemiAtePackage.get_fields()
        all_package_names.extend(RequiredPackage.get_fields())

        available_packages = EnvironmentHandler.get_available_packages_version(all_package_names)

        installed_packages = EnvironmentHandler.get_installed_packages(env_name)
        installed_packages = filter(lambda package: package.name in all_package_names, installed_packages)

        available_packages_dict = {package.name: package for package in available_packages}
        installed_packages_dict = {package.name: package for package in installed_packages}
        
        to_update = []

        for package_name, available_package in available_packages_dict.items():
            installed_package = installed_packages_dict.get(package_name)
            if not installed_package:
                # is it an issue if packages are not available ??
                continue

            if installed_package.version < available_package.version:
                to_update.append((available_package.name, installed_package.version, available_package.version))

        return to_update

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
        return Repository.get_available_versions(joined_packages)

    @staticmethod
    def install_packages(handler_type: HandlerType, env_name: str, packages: List[str]):
        if handler_type == HandlerType.Mamba:
            MambaEnvHandler.install_packages(env_name, packages)
        else:
            CondaEnvHandler.install_packages(env_name, packages)


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
        run_command(Commands.INSTALL, '-n', env_name, '-c', 'conda-forge', *packages, '-y', use_exception_handler=False, stdout=sys.stdout)
