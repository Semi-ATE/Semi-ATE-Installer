from dataclasses import dataclass
from enum import Enum
from numbers import Number
from typing import List


class SemiAtePackage(Enum):
    Common = 'semi-ate-common'
    ProjectDatabase = 'semi-ate-project-database'
    Sammy = 'semi-ate-sammy'
    Plugins = 'semi-ate-plugins'
    Spyder = 'semi-ate-spyder'    
    Testers = 'semi-ate-testers'
    AppsCommon = 'semi-ate-apps-common'
    ControlApp = 'semi-ate-control-app'
    MasterApp = 'semi-ate-master-app'
    TestApp = 'semi-ate-test-app'

    def __call__(self) -> str:
        return self.value


class RequiredPackage(Enum):
    Spyder = 'spyder'
    Mosquitto = 'mosquitto'
    SemiAteStdf = 'semi-ate-stdf'

    def __call__(self) -> str:
        return self.value


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
