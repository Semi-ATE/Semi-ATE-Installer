from dataclasses import dataclass
from enum import Enum
from numbers import Number
from typing import List

from semi_ate_installer.utils import BaseDataClass


class PackageHandler:
    @staticmethod
    def get_test_program_developer_packages() -> List[str]:
        packages = SemiAtePackage.get_fields()
        packages.extend(RequiredPackage.get_fields())
        return packages


@dataclass
class SemiAtePackage(BaseDataClass):
    Common: str = 'semi-ate-common'
    ProjectDatabase: str = 'semi-ate-project-database'
    Sammy: str = 'semi-ate-sammy'
    Plugins: str = 'semi-ate-plugins'
    Spyder: str = 'semi-ate-spyder'    
    Testers: str = 'semi-ate-testers'
    AppsCommon: str = 'semi-ate-apps-common'
    ControlApp: str = 'semi-ate-control-app'
    MasterApp: str = 'semi-ate-master-app'
    TestApp: str = 'semi-ate-test-app'


@dataclass
class RequiredPackage(BaseDataClass):
    Spyder: str = 'spyder'
    Mosquitto: str = 'mosquitto'
    SemiAteStdf: str = 'semi-ate-stdf'


@dataclass
class InstalledPackageInfo:
    name: str
    version: str


@dataclass
class AvailablePackageInfo:
    name: str
    versions: set

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __hash__(self) -> Number:
        return len(self.name) + len(self.versions)
