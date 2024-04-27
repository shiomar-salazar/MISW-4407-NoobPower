
import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.engine.service_locator import ServiceLocator

def create_square(ecs_world:esper.World, size:pygame.Vector2,
                    pos:pygame.Vector2, vel:pygame.Vector2, col:pygame.Color):
    cuad_entity = ecs_world.create_entity()
    ecs_world.add_component(cuad_entity,
                CSurface(size, col))
    ecs_world.add_component(cuad_entity,
                CTransform(pos))
    ecs_world.add_component(cuad_entity, 
                CVelocity(vel))
    
def create_sprite(world: esper.World, pos: pygame.Vector2, surface: pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity, CTransform(pos))
    world.add_component(sprite_entity, CSurface.from_surface(surface))
    return sprite_entity


def create_enemy_square(world: esper.World, pos: pygame.Vector2, enemy_info: dict):
    enemy_surface = ServiceLocator.images_service.get(enemy_info["image"])
    size = enemy_surface.get_size()
    size = (size[0] / enemy_info["animations"]["number_frames"], size[1])
    position = pygame.Vector2(pos[0] - (size[0] / 2),  pos[1] - (size[1] / 2))
    enemy_entity = create_sprite(world, position, enemy_surface)
    world.add_component(enemy_entity, CAnimation(enemy_info["animations"]))
    world.add_component(enemy_entity, CTagEnemy())

def create_level(ecs_world:esper.World, enemies_data:dict, level_data:dict, window_data:dict):
    midle_point = window_data["size"]["w"] / 2
    j = 90
    for row in level_data.keys():
        if(row != "fila6"):
            x_mod = 8
        else:
            x_mod = 24
        
        for i in range(level_data[row]["count"]):
            if( i % 2 == 0 and i !=0):
                x_mod += 16
            create_enemy_square(ecs_world,pygame.Vector2(midle_point + x_mod,j),enemies_data[level_data[row]["enemy_type"]])
            x_mod *= -1
        j -= 12
