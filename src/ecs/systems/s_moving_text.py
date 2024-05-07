import esper
from src.ecs.components.c_transform import CTransform

def system_moving_text(world:esper.World, delta_time:float):
    components = world.get_component(CTransform)

    c_t:CTransform
    for  (_, c_t) in components:
        if c_t.pos.y <= 25:
            return
        c_t.pos.y -= 50 * delta_time