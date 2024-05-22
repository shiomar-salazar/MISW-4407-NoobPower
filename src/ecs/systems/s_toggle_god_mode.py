
import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_toggle_god_mode(world:esper.World):
    component_player = world.get_components(CSurface, CTransform, CTagPlayer)
    for _, (c_s, c_t, c_t_p) in component_player:
        if c_s.visible == True:
            c_t_p._godMode = not c_t_p._godMode
        return c_t_p._godMode