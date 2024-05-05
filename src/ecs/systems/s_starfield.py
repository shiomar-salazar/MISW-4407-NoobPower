import random

import pygame
import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_star import CTagStar


def system_starfield(world:esper.World, delta_time:float, stars_info: dict, window_info: dict):
    components = world.get_components(CSurface, CTransform, CTagStar)
    star_colors = stars_info["star_colors"]
    blink_rate = stars_info["blink_rate"]
    number_of_stars = stars_info["number_of_stars"]

    stars_on_screen = 0

    for _, (c_s, c_t, _) in components:
        if stars_on_screen >= number_of_stars:
            break

        c_t.pos.y += random.uniform(stars_info["vertical_speed"]["min"], stars_info["vertical_speed"]["max"]) * delta_time

        if c_t.pos.y > window_info["size"]["h"]:
            c_t.pos.y = random.randint(0, window_info["size"]["h"])
            c_t.pos.x = random.randint(0, window_info["size"]["w"])

        color = random.choice(star_colors)
        pygame.draw.circle(c_s.surf, pygame.Color(color["r"], color["g"], color["b"]), (0, 0), 1)

        if random.random() < blink_rate["min"]:
            pygame.draw.circle(c_s.surf, pygame.Color(window_info["bg_color"]["r"], window_info["bg_color"]["g"], window_info["bg_color"]["b"]), (0, 0), 1)

        stars_on_screen += 1

