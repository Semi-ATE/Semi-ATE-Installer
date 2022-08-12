from dataclasses import dataclass
from enum import Enum
from numbers import Number
from typing import List

from semi_ate_installer.utils import BaseDataClass


@dataclass
class PackageInfo:
    name: str
    version: str

    def __hash__(self) -> Number:
        return len(self.name) + len(self.version)


@dataclass
class SemiAtePackage(BaseDataClass):
    Spyder: str = 'semi-ate-spyder'    
    Testers: str = 'semi-ate-testers'
    ControlApp: str = 'semi-ate-control-app'
    MasterApp: str = 'semi-ate-master-app'
    TestApp: str = 'semi-ate-test-app'


@dataclass
class RequiredPackage(BaseDataClass):
    Spyder: str = 'spyder'
    Mosquitto: str = 'mosquitto'
    SemiAteStdf: str = 'semi-ate-stdf'
