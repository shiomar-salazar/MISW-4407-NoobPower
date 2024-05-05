import random
import esper
from src.create.prefab_creator import create_enemy_bullet
from src.ecs.components.c_reload import CReload
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet


def system_enemy_fire(world: esper.World, delta_time: float, bullet_info: dict):
    enemy_bullets_count = len(world.get_component(CTagEnemyBullet))
    if enemy_bullets_count >= bullet_info["enemy_bullet"]["max_enemy_bullets"]:
         return
    for entity, (c_transform, _, c_reload) in world.get_components(CTransform, CSurface, CReload):
        if world.has_component(entity, CTagEnemy):
            c_reload.current_time -= delta_time
            if c_reload.current_time <= 0 and random.random() < bullet_info["enemy_bullet"]["fire_prob"]:  #* Añade una probabilidad de disparo
                create_enemy_bullet(world, c_transform.pos, bullet_info)
                c_reload.current_time = c_reload.reload_time