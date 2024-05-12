import random

import pygame
import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_star import CTagStar


def system_starfield(world: esper.World, delta_time: float, stars_info: dict, window_info: dict):
    components = world.get_components(CSurface, CTransform, CTagStar)
    star_colors = stars_info["star_colors"]
    blink_rate = stars_info["blink_rate"]

    for _, (c_s, c_t, _) in components:
        c_t.pos.y += random.uniform(stars_info["vertical_speed"]["min"], stars_info["vertical_speed"]["max"]) * delta_time

        if c_t.pos.y > window_info["size"]["h"]:
            c_t.pos.y = 0
            c_t.pos.x = random.randint(0, window_info["size"]["w"])
            color = random.choice(star_colors)
            c_s.color = color 
            c_s.surf.fill(pygame.Color(color["r"], color["g"], color["b"]))

        if random.random() < blink_rate["min"]:
            c_s.surf.set_alpha(0)
        elif random.random() > blink_rate["max"]:
            c_s.surf.set_alpha(255)
        else:

            alpha = 0 if random.random() < 0.5 else 255
            c_s.surf.set_alpha(alpha)


