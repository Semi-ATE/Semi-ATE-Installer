from enum import Enum

class Profile(Enum):

    TestProgramDeveloper = 'test program developer'

    def __call__(self):
        return self.value