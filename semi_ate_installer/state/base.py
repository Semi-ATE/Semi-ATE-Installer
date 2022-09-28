from abc import ABC, abstractclassmethod
from enum import IntEnum
import sys


class State(IntEnum):
    Done = 0
    Next = 1


class BaseState(ABC):
    @abstractclassmethod
    def next(self) -> 'BaseState':
        pass


class BaseStateWithInput(BaseState):
    def __init__(self, *inputs) -> None:
        for input in inputs:
            if not input:
                sys.exit()


class BaseStateMachine(ABC):
    def next(self) -> 'BaseState':
        pass
    
    def is_done(self) -> State:
        pass
