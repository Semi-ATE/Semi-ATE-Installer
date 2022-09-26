from enum import IntEnum
from typing import List, Tuple
import questionary
from questionary import Choice
from packaging import version

from semi_ate_installer.environment.handler import EnvironmentHandler, HandlerType
from semi_ate_installer.utils.profiles import Profiles
from semi_ate_installer.state.base import BaseState, BaseStateMachine, BaseStateWithInput, State


HANDLER_TYPE = HandlerType.Mamba


class InitOptions(IntEnum):
    New = 0
    Exist = 1


class YesNoOption(IntEnum):
    No = 0
    Yes = 1


class Init(BaseState):
    def next(self) -> BaseState:
        new = Choice('create new environment: ', value=InitOptions.New)
        exist = Choice('list available environments: ', value=InitOptions.Exist)
        option = questionary.select('select option: ', [new, exist], ).ask()

        if option == InitOptions.Exist:
            existing_envs = EnvironmentHandler.get_available_environments()
            return SelectEnv(existing_envs)
        else:
            return NewEnv()


class SelectEnv(BaseStateWithInput):
    def __init__(self, env_list: List[str]):
        super().__init__(env_list)
        self.env_list = env_list

    def next(self) -> BaseState:
        selected_env = questionary.select('select environment of interest', self.env_list).ask()
        return CheckPackagesUpdate(selected_env)


class CheckPackagesUpdate(BaseStateWithInput):
    def __init__(self, env_name: str):
        super().__init__(env_name)
        self.env_name = env_name

    def next(self) -> BaseState:
        available_updates = EnvironmentHandler.get_available_updates(self.env_name)
        if available_updates:
            return UpdatePackages(self.env_name, available_updates)

        return EnvSelected(self.env_name)

class UpdatePackages(BaseStateWithInput):
    def __init__(self, env_name: str, available_updates: List[Tuple[str, version.Version, version.Version]]):
        super().__init__(env_name)
        self.env_name = env_name
        self.available_updates = available_updates

    def next(self) -> BaseState:
        print('update for the following packages is available: ')
        for available_update in self.available_updates:
            print(f'{available_update[0]}: {available_update[1]} -> {available_update[2]}')

        no = Choice('no:', value=YesNoOption.No)
        yes = Choice('yes:', value=YesNoOption.Yes)
        option = questionary.select('updates are available, do update:', [no, yes], ).ask()

        if option == YesNoOption.No:
            return EnvSelected(self.env_name)

        package_to_update = [name for name, _, _ in self.available_updates]
        EnvironmentHandler.install_packages(HANDLER_TYPE, self.env_name, package_to_update)


class NewEnv(BaseState):
    def next(self) -> BaseState:
        env_name = questionary.text('insert the new environment name:', validate=lambda input: input is not None).ask()
        if not env_name:
            print(f'environment name is empty')
            return None

        existing_envs = EnvironmentHandler.get_available_environments()
        if env_name in existing_envs:
            print(f'environment: \'{env_name}\' exists already')
            return None

        return SelectProfile(env_name)


class SelectProfile(BaseStateWithInput):
    def __init__(self, env_name: str):
        super().__init__(env_name)
        self.env_name = env_name

    def next(self) -> BaseState:
        selected_profile = questionary.select('select profile', Profiles.get_fields()).ask()
        return CreateEnv(self.env_name, selected_profile)


class CreateEnv(BaseStateWithInput):
    def __init__(self, env_name: str, profile: str):
        super().__init__(env_name, profile)
        self.env_name = env_name
        self.profile = profile

    def next(self) -> BaseState:
        packages = EnvironmentHandler.get_packages(self.profile)
        EnvironmentHandler.create_env(HANDLER_TYPE, self.env_name)
        EnvironmentHandler.install_packages(HANDLER_TYPE, self.env_name, packages)
        return EnvSelected(self.env_name)


class EnvSelected(BaseStateWithInput):
    def __init__(self, env_name: str):
        super().__init__(env_name)
        self.env_name = env_name

    def next(self) -> BaseState:
        EnvironmentHandler.print_activate(self.env_name)
        return Done()


class Done(BaseState):
    def next(self) -> BaseState:
        return None


class NewEnvSM(BaseStateMachine):
    def __init__(self):
        self.state = Init()

    def next(self) -> BaseState:
        self.state = self.state.next()
        return None

    def is_done(self) -> State:
        return State.Done if self.state is None else State.Next
