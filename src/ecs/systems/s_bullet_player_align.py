import esper
from src.create.prefab_creator import create_bullet
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet

def system_bullet_player_align(world:esper.World, bullet_cfg:dict):

    player_components = world.get_components(CSurface, CTransform, CTagPlayer)
    bullet_components = world.get_components(CVelocity, CTransform, CSurface, CTagPlayerBullet)

    for _, (c_p_s,c_p_t,c_t_p) in player_components:
        if not c_t_p._invencible:
            for _, (c_v,c_t,c_s, _) in bullet_components:
                if c_v.vel.y == 0:
                    c_t.pos.x = c_p_t.pos.x + c_p_s.area.size[0] / 2
            if(len(bullet_components) == 0):
                create_bullet(world, c_p_t.pos, c_p_s.area.size, bullet_cfg) 