import pygame
import esper
from src.create.prefab_creator import create_explosion
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_blinking import CBlinking
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet

def system_collision_player_bullet(world:esper.World, explosion_data:dict, delta_time:float, screen:pygame.Surface):
    component_player = world.get_components(CSurface, CTransform, CTagPlayer)
    components_enemy_bullet = world.get_components(CSurface, CTransform, CTagEnemyBullet)
    component_player_bullet = world.get_component(CTagPlayerBullet)

    for _, (c_s, c_t, c_t_p) in component_player:
        if c_t_p._invencible:
            c_t_p.actual_time += delta_time

        if c_t_p.actual_time >= 3:
            ps_size = c_s.surf.get_size()
            c_t.pos.x = screen.get_rect().midbottom[0] - ps_size[0]/2
            c_t.pos.y = screen.get_rect().midbottom[1] - ps_size[1]/2 - 15
            c_t_p._invencible = False
            c_s.visible = True
            c_t_p.actual_time = 0
            text_entities = world.get_components(CSurface, CTransform,CBlinking)
            for entity, (_,_,_) in text_entities:
                world.delete_entity(entity)
            

        player_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        for enemy_bullet_ent, (c_b_s, c_b_t, _) in components_enemy_bullet:
            enemy_bullet_rect = CSurface.get_area_relative(c_b_s.area, c_b_t.pos)
            if player_rect.colliderect(enemy_bullet_rect) and c_t_p._invencible == False and c_t_p._godMode == False:
                
                world.delete_entity(enemy_bullet_ent)
                for entity ,_ in component_player_bullet:
                    world.delete_entity(entity)
                create_explosion(world, c_t.pos, explosion_data, True)
                c_t_p._invencible = True
                c_s.visible = False
                return True
    return False
                