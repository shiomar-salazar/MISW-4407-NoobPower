import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.engine.service_locator import ServiceLocator

def system_bullet_shoot(world:esper.World, bullet_cfg:dict):

    bullet_components = world.get_components(CVelocity, CTransform, CTagPlayerBullet)

    for _, (c_v,c_t,_) in bullet_components:
        if c_v.vel.y == 0:
            c_v.vel.y = bullet_cfg["velocity"]*-1
            ServiceLocator.sounds_service.play(bullet_cfg["sound"])