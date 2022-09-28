from enum import Enum

class Command(Enum):
    InstallProfile = 'Install profile'
    UpdateSemiAtePackages = 'Update SemiATE Packages'
    UpdateRequiredPackages = 'Update required Packages'
    RemoveSemiAtePackages = 'Remove all SemiATE Packages'
    Exit = 'Exit'

    def __call__(self) -> str:
        return self.value
