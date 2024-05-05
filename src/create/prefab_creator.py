
import random
import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.components.tags.c_tag_star import CTagStar
from src.engine.service_locator import ServiceLocator

def create_square(ecs_world:esper.World, size:pygame.Vector2,
                    pos:pygame.Vector2, vel:pygame.Vector2, col:pygame.Color):
    cuad_entity = ecs_world.create_entity()
    ecs_world.add_component(cuad_entity, CSurface(size, col))
    ecs_world.add_component(cuad_entity, CTransform(pos))
    ecs_world.add_component(cuad_entity,  CVelocity(vel))
    return cuad_entity
    
def create_sprite(world: esper.World, pos: pygame.Vector2, vel: pygame.Vector2, surface: pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity, CTransform(pos))
    world.add_component(sprite_entity, CVelocity(vel))
    world.add_component(sprite_entity, CSurface.from_surface(surface))
    return sprite_entity

def create_enemy_square(world: esper.World, pos: pygame.Vector2, enemy_info: dict, movement_vel: int):
    enemy_surface = ServiceLocator.images_service.get(enemy_info["image"])
    size = enemy_surface.get_size()
    size = (size[0] / enemy_info["animations"]["number_frames"], size[1])
    position = pygame.Vector2(pos[0] - (size[0] / 2),  pos[1] - (size[1] / 2))
    vel = pygame.Vector2(movement_vel,0)
    enemy_entity = create_sprite(world, position, vel, enemy_surface)
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
            create_enemy_square(ecs_world,pygame.Vector2(midle_point + x_mod,j),enemies_data[level_data[row]["enemy_type"]], enemies_data["movement_velocity"])
            x_mod *= -1
        j -= 12

def create_input_player(world: esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_fire = world.create_entity()
    world.add_component(input_fire,CInputCommand("PLAYER_FIRE", pygame.K_z))
    world.add_component(input_left, CInputCommand('PLAYER_LEFT', pygame.K_LEFT))
    world.add_component(input_right, CInputCommand('PLAYER_RIGHT', pygame.K_RIGHT))

def create_bullet(world: esper.World, player_pos: pygame.Vector2,
                  player_size: pygame.Vector2, bullet_info: dict):
    
    size = pygame.Vector2(bullet_info["size"]["x"], bullet_info["size"]["y"])
    color = pygame.Color(bullet_info["color"]["r"], bullet_info["color"]["g"], bullet_info["color"]["b"])
    pos = pygame.Vector2(player_pos.x + player_size[0] / 2, player_pos.y + player_size[1] / 2)
    vel = pygame.Vector2(0, bullet_info["velocity"]*-1)

    bullet_entity = create_square(world, size, pos, vel, color)
    world.add_component(bullet_entity, CTagPlayerBullet())
    ServiceLocator.sounds_service.play(bullet_info["sound"])

def create_player(world:esper.World, player_info:dict, screen:pygame.Surface):
    player_surface = ServiceLocator.images_service.get(player_info["image"])
    ps_size = player_surface.get_size() 
    position_o = pygame.Vector2(screen.get_rect().midbottom[0] - ps_size[0]/2, screen.get_rect().midbottom[1] - ps_size[1]/2 - 15)
    velocity_o = pygame.Vector2(0,0)
    player_entity = create_sprite(world, position_o, velocity_o, player_surface)
    world.add_component(player_entity, CTagPlayer())
    return player_entity

def create_explosion(world:esper.World, pos:pygame.Vector2, explosion_info:dict):
    explosion_surface = ServiceLocator.images_service.get(explosion_info["image"])
    vel = pygame.Vector2(0, 0)
    explosion_ent = create_sprite(world, pos, vel, explosion_surface)
    world.add_component(explosion_ent, CTagExplosion())
    world.add_component(explosion_ent, CAnimation(explosion_info["animations"]))
    ServiceLocator.sounds_service.play(explosion_info["sound"])
    return explosion_ent

def create_stars(world: esper.World, stars_info: dict, window_info: dict):
    for _ in range(stars_info["number_of_stars"]):
        x = random.randint(0, window_info["size"]["w"])
        y = random.randint(0, window_info["size"]["h"])
        star_color = random.choice(stars_info["star_colors"])
        color = pygame.Color(star_color["r"], star_color["g"], star_color["b"])
        star_entity = create_square(world, pygame.Vector2(1, 1), pygame.Vector2(x, y), pygame.Vector2(0, 0), color)
        world.add_component(star_entity, CTagStar())