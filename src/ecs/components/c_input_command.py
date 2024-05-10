from enum import Enum
import pygame


class CInputCommand:
    def __init__(self, name: str, key: int) -> None:
        self.name = name
        self.key = key
        self.phase = CommandPhase.NA

class CommandPhase(Enum):
    NA = 0
    START = 1
    END = 2
    ACTIVE = 3
    INACTIVE = 4
