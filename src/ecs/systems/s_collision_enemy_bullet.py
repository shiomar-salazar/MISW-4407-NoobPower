import esper
from src.create.prefab_creator import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet


def system_collision_enemy_bullet(world:esper.World, explosion_data:dict):
    components_enemy = world.get_components(CSurface, CTransform, CTagEnemy)
    components_bullet = world.get_components(CSurface, CTransform, CTagPlayerBullet)

    for enemy_ent, (c_s, c_t, _) in components_enemy:
        enem_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        for bullet_ent, (c_b_s, c_b_t, _) in components_bullet:
            bullet_rect = CSurface.get_area_relative(c_b_s.area, c_b_t.pos)
            if enem_rect.colliderect(bullet_rect):
                world.delete_entity(enemy_ent)
                world.delete_entity(bullet_ent)
                create_explosion(world, c_t.pos, explosion_data)