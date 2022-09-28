import sys
from typing import List, Tuple
import re
from conda.cli.python_api import Commands, run_command

from packaging import version

from semi_ate_installer.channel.repository import Repository
from semi_ate_installer.utils.packages import RequiredPackage, SemiAtePackage, PackageInfo
from semi_ate_installer.utils.profiles import Profiles


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
    def install_packages(env_name: str, packages: List[str]) -> None:
        CondaEnvHandler.install_packages(env_name, packages)

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
    def create_env(env_name: str, packages: List[str] = []):
        CondaEnvHandler.create_env(env_name, packages)

    @staticmethod
    def get_packages(profile: str) -> List[str]:
        return {
            Profiles.TestProgramDeveloper: EnvironmentHandler.get_test_program_developer_packages
        }[profile]()

    @staticmethod
    def print_activate(env_name: str):
        message = (
            "\nTo activate this environment, use\n\n"
            f"     $ conda activate {env_name}\n\n"
            "To deactivate an active environment, use\n\n"
            "     $ conda deactivate\n"
        )
        print(message)

    @staticmethod
    def get_packages_with_version(package_names: List[str]) -> List[PackageInfo]:
        available_packages = [package_info for package_info in EnvironmentHandler.get_available_packages_version(package_names) if package_info.name in SemiAtePackage.get_fields()]
        available_packages_dict = {package.name: package for package in available_packages}
        minor_package_version = EnvironmentHandler._get_minor_package_version(available_packages_dict)
        package_list = []

        package_list = [f'{package_name}={minor_package_version.version}' for package_name in SemiAtePackage.get_fields()]
        rest_packages = set(package_names) - set(SemiAtePackage.get_fields())
        package_list.extend(rest_packages)

        return package_list

    @staticmethod
    def get_available_updates(env_name: str) -> List[Tuple[str, version.Version, version.Version]]:
        all_package_names = SemiAtePackage.get_fields()
        all_package_names.extend(RequiredPackage.get_fields())

        available_packages = EnvironmentHandler.get_available_packages_version(all_package_names)

        installed_packages = EnvironmentHandler.get_installed_packages(env_name)
        installed_packages = filter(lambda package: package.name in all_package_names, installed_packages)

        available_packages_dict = {package.name: package for package in available_packages}
        installed_packages_dict = {package.name: package for package in installed_packages}

        minor_package_version = EnvironmentHandler._get_minor_package_version(available_packages_dict)
        
        to_update = []

        for package_name, _ in available_packages_dict.items():
            if package_name not in SemiAtePackage.get_fields():
                continue

            installed_package = installed_packages_dict.get(package_name)
            if not installed_package:
                # is it an issue if packages are not available ??
                continue

            if installed_package.version != minor_package_version.version:
                to_update.append((package_name, installed_package.version, minor_package_version))

        return to_update

    def _get_minor_package_version(available_packages: dict):
        from functools import reduce
        only_semi_ate_packages = filter(lambda package: package.name in SemiAtePackage.get_fields(), available_packages.values())
        def compare(lhs: PackageInfo, rhs: PackageInfo) -> bool:
            if lhs.version < rhs.version:
                return lhs

            return rhs

        return reduce(compare, only_semi_ate_packages)

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
    def install_packages(env_name: str, packages: List[str]):
        CondaEnvHandler.install_packages(env_name, packages)


class CondaEnvHandler:
    @staticmethod
    def create_env(env_name: str, packages: List[str] =[]):
        from conda.cli.python_api import Commands, run_command
        run_command(Commands.CREATE, '-n', env_name, 'python=3', *packages, '-y', use_exception_handler=False, stdout=sys.stdout)

    @staticmethod
    def install_packages(env_name: str, packages: List[str]):
        from conda.cli.python_api import Commands, run_command
        run_command(Commands.INSTALL, '-n', env_name, '-c', 'conda-forge', *packages, '-y', use_exception_handler=False, stdout=sys.stdout)
