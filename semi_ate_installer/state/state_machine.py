from enum import IntEnum
from typing import List
from environment.handler import Environment, EnvironmentHandler
import questionary
from questionary import Choice

from semi_ate_installer.state.base import BaseState, BaseStateMachine, BaseStateWithInput, State


class InitOptions(IntEnum):
    New = 0
    Exist = 1


# check for empty selection lists

class Init(BaseState):
    def next(self) -> BaseState:
        new = Choice('create new env', value=InitOptions.New)
        exist = Choice('select env', value=InitOptions.Exist)
        option = questionary.select('select option: ', [new, exist], ).ask()

        if option == InitOptions.Exist:
            existing_envs = EnvironmentHandler.get_available_environments()
            selectable_envs = [e.name for e in existing_envs]
            return SelectEnv(selectable_envs)
        else:
            return NewEnv()


class SelectEnv(BaseStateWithInput):
    def __init__(self, env_list: List[str]):
        super().__init__(env_list)
        self.env_list = env_list

    def next(self):
        selected_env = questionary.select('Select environment of interest', self.env_list).ask()
        return ActivateEnv(selected_env)


class NewEnv(BaseState):
    def __init__(self) -> None: pass

    def next(self) -> BaseState:
        env_name = questionary.text('insert the new environment name:', validate=lambda input: input is not None).ask()
        existing_envs = [env.name for env in EnvironmentHandler.get_available_environments()]

        if env_name in existing_envs:
            print(f'environment: \'{env_name}\' exists already')
            return None

        return ActivateEnv(env_name)


class SelectProfile(BaseStateWithInput):
    def __init__(self, env_name: str) -> None:
        super().__init__(env_name)
        self.env_name = env_name

    def next(self) -> BaseState:
        all_profiles = []
        selected_profile = questionary.select('Select environment of interest', all_profiles).ask()
        return CreateEnv(self.env_name, selected_profile)


class CreateEnv(BaseStateWithInput):
    def __init__(self, env_name: str, profile: str) -> None:
        super().__init__(env_name, profile)
        self.env_name = env_name
        self.profile = profile

    def next(self) -> BaseState:
        return ActivateEnv(self.env_name)


class ActivateEnv(BaseStateWithInput):
    def __init__(self, env_name: str) -> None:
        super().__init__(env_name)
        self.env_name = env_name

    def next(self) -> BaseState:
        print(f'env: {self.env_name} is activated :)')
        return Done()


class Done(BaseState):
    def next(self) -> BaseState:
        return None


class NewEnvSM(BaseStateMachine):
    def __init__(self) -> None:
        self.state = Init()

    def next(self) -> BaseState:
        self.state = self.state.next()

    def is_done(self) -> State:
        print(self.state)
        return State.Done if self.state is None else State.Next
