import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity

def system_bullet_player_align(world:esper.World, player_ent:int, bullet_ent:int):
    player_c_t = world.component_for_entity(player_ent, CTransform)
    player_c_s = world.component_for_entity(player_ent, CSurface)
    bullet_c_t = world.component_for_entity(bullet_ent, CTransform)
    bullet_c_v = world.component_for_entity(bullet_ent, CVelocity)

    if bullet_c_v.vel.y == 0:
        bullet_c_t.pos.x = player_c_t.pos.x + player_c_s.area.size[0] / 2 - 1