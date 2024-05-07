import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_blinking import CBlinking
from src.ecs.components.c_transform import CTransform


def system_blinking_text(world:esper.World, delta_time:float):
    components = world.get_components(CSurface, CBlinking)
    c_s:CSurface
    c_b:CBlinking
    for _, (c_s, c_b) in components:
        c_b.actual_time += delta_time
        if c_b.actual_time >= 0.5:
            c_s.surf.set_alpha(c_b.alpha)
            c_b.actual_time = 0
            if c_b.alpha == 255:
                c_b.alpha = 0
            else:
                c_b.alpha = 255

