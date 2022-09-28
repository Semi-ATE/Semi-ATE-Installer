from dataclasses import dataclass, fields
from enum import Enum
from typing import List

from semi_ate_installer.utils import BaseDataClass


@dataclass
class Profiles(BaseDataClass):
    TestProgramDeveloper: str = 'test program developer'
