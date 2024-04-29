
import pygame
import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player import CTagPlayer

"""
    Sistema para controlar los limites de la pantalla del jugador
"""
def system_player_limits(world:esper.World, screen: pygame.Surface):
    components = world.get_components(CTransform, CVelocity, CSurface, CTagPlayer)
    screen_rect = screen.get_rect()
    c_s:CSurface
    for _, (c_t, c_v, c_s, _) in components:
        player_rect = c_s.surf.get_rect(topleft=c_t.pos)
        outside = False
        if player_rect.left < 0 or player_rect.right > screen_rect.width:
            outside = True

        if outside:
            player_rect.clamp_ip(screen_rect)
            c_t.pos.y = player_rect.y
            c_t.pos.x = player_rect.x