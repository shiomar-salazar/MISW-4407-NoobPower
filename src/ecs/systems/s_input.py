from typing import Callable
import pygame
import esper
from src.ecs.components.c_input_command import CInputCommand, CommandPhase


def system_input(world: esper.World,
                        event: pygame.event.Event,
                        do_action: Callable[[CInputCommand], None]):
    components = world.get_component(CInputCommand)
    for _, c_input in components:
        if event.type == pygame.KEYDOWN and c_input.key == event.key:
            if c_input.name == "PAUSE":
                if c_input.phase != CommandPhase.ACTIVE:
                    c_input.phase = CommandPhase.ACTIVE
                    do_action(c_input)
                else:
                    c_input.phase = CommandPhase.INACTIVE
                    do_action(c_input)
            else:
                c_input.phase = CommandPhase.START
                do_action(c_input)
        elif event.type == pygame.KEYUP and c_input.key == event.key:
            if c_input.name != "PAUSE":
                c_input.phase = CommandPhase.END
                do_action(c_input)
            else:
                pass
