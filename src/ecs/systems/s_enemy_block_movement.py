import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_enemy_block_movement(world: esper.World, delta_time: float, screen_width: int):
    min_x = screen_width
    max_x = 0
    for entity, (c_transform, c_velocity, c_surface) in world.get_components(CTransform, CVelocity, CSurface):
        if world.has_component(entity, CTagEnemy):
            #* En min_x dividí por 3 porque encontré que así rebotaba a la misma distancia a la izquierda y derecha, pero no tengo una justificación clara, se podría revisar.
            min_x = min(min_x, c_transform.pos.x - c_surface.surf.get_width() / 3)
            max_x = max(max_x, c_transform.pos.x + c_surface.surf.get_width() / 2)
            #print(screen_width, max_x, max_x > screen_width)

    if min_x < 0 or max_x > screen_width:
        for entity, (_, c_velocity) in world.get_components(CTransform, CVelocity):
            if world.has_component(entity, CTagEnemy):
                c_velocity.vel.x *= -1

    for entity, (c_transform, c_velocity) in world.get_components(CTransform, CVelocity):
        if world.has_component(entity, CTagEnemy):
            c_transform.pos.x += c_velocity.vel.x * delta_time