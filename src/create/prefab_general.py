import random
import esper
import pygame
from src.create.prefab_creator import create_square
from src.ecs.components.tags.c_tag_star import CTagStar

def create_stars(world: esper.World, stars_info: dict, window_info: dict):
    for _ in range(stars_info["number_of_stars"]):
        x = random.randint(0, window_info["size"]["w"])
        y = random.randint(0, window_info["size"]["h"])
        star_color = random.choice(stars_info["star_colors"])
        color = pygame.Color(star_color["r"], star_color["g"], star_color["b"])
        star_entity = create_square(world, pygame.Vector2(1, 1), pygame.Vector2(x, y), pygame.Vector2(0, 0), color)
        world.add_component(star_entity, CTagStar())