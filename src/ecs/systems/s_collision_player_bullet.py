import pygame
import esper
from src.create.prefab_creator import create_explosion, create_player
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_collision_player_bullet(world:esper.World, explosion_data:dict, player_cfg:dict, screen:pygame.Surface):
    component_player = world.get_components(CSurface, CTransform, CTagPlayer)
    components_enemy_bullet = world.get_components(CSurface, CTransform, CTagEnemyBullet)
    componen_input = world.get_component(CInputCommand)

    for player_ent, (c_s, c_t, _) in component_player:
        player_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        for enemy_bullet_ent, (c_b_s, c_b_t, _) in components_enemy_bullet:
            enemy_bullet_rect = CSurface.get_area_relative(c_b_s.area, c_b_t.pos)
            if player_rect.colliderect(enemy_bullet_rect):
                world.delete_entity(player_ent)
                world.delete_entity(enemy_bullet_ent)
                create_explosion(world, c_t.pos, explosion_data)
                for input_ent, c_i in componen_input:
                    world.delete_entity(input_ent)
                return True
    return False