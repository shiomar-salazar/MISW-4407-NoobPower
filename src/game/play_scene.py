import json

import pygame

from src.create.prefab_creator import create_bullet, create_input_player, create_level, create_player, create_stars
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_collision_enemy_bullet import system_collision_enemy_bullet
from src.ecs.systems.s_enemy_block_movement import system_enemy_block_movement
from src.ecs.systems.s_enemy_fire import system_enemy_fire
from src.ecs.systems.s_explosion_kill import system_explosion_kill
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_limits import system_player_limits
from src.ecs.systems.s_screen_bullet import system_screen_bullet
from src.ecs.systems.s_starfield import system_starfield
from src.engine.scenes.scene import Scene
from src.engine.service_locator import ServiceLocator


class PlayScene(Scene):
    def __init__(self, engine:'src.engine.game_engine.GameEngine', screen_surf:pygame.Surface) -> None:
        super().__init__(engine)
        self.window_cfg = ServiceLocator.configurations_service.get("assets/cfg/window.json")
        self.enemies_cfg  = ServiceLocator.configurations_service.get("assets/cfg/enemies.json")
        self.level_cfg = ServiceLocator.configurations_service.get("assets/cfg/enemy_field.json")
        self.bullet_cfg = ServiceLocator.configurations_service.get("assets/cfg/bullet.json")
        self.player_cfg = ServiceLocator.configurations_service.get("assets/cfg/player.json")
        self.explosion_cfg = ServiceLocator.configurations_service.get("assets/cfg/explosion.json")
        self.starfield_cfg = ServiceLocator.configurations_service.get("assets/cfg/starfield.json")
        self._screen_surf = screen_surf

    def do_create(self):
        self.player_entity = create_player(self.ecs_world, self.player_cfg, self._screen_surf)
        self.player_c_v = self.ecs_world.component_for_entity(self.player_entity, CVelocity)
        self.player_c_t = self.ecs_world.component_for_entity(self.player_entity, CTransform)
        self.player_c_s = self.ecs_world.component_for_entity(self.player_entity, CSurface)
        create_level(self.ecs_world, self.enemies_cfg, self.level_cfg, self.window_cfg)
        create_input_player(self.ecs_world)
        create_stars(self.ecs_world, self.starfield_cfg, self.window_cfg)

    def do_update(self, delta_time: float):
        system_starfield(self.ecs_world, delta_time, self.starfield_cfg, self.window_cfg)
        system_movement(self.ecs_world, delta_time)
        system_enemy_block_movement(self.ecs_world, delta_time, self.window_cfg["size"]["w"])
        system_enemy_fire(self.ecs_world, delta_time, self.bullet_cfg)
        system_screen_bullet(self.ecs_world, self._screen_surf)
        system_player_limits(self.ecs_world, self._screen_surf)
        system_collision_enemy_bullet(self.ecs_world, self.explosion_cfg["enemy_explosion"])
        system_explosion_kill(self.ecs_world)
        system_animation(self.ecs_world, delta_time)
        self.ecs_world._clear_dead_entities()
        self.player_bullets = len(self.ecs_world.get_component(CTagPlayerBullet))
        
    def do_action(self, action: CInputCommand):
        if action.name == "PLAYER_FIRE" and action.phase == CommandPhase.START and self.player_bullets == 0:
            create_bullet(self.ecs_world, self.player_c_t.pos,
                          self.player_c_s.area.size, self.bullet_cfg)
        #Input de movimiento del jugador
        elif action.name == 'PLAYER_LEFT':
            if action.phase == CommandPhase.START:
                self.player_c_v.vel.x -= self.player_cfg['input_velocity']
                
            elif action.phase == CommandPhase.END:
                self.player_c_v.vel.x += self.player_cfg['input_velocity']

        elif action.name == 'PLAYER_RIGHT':
            if action.phase == CommandPhase.START:
                    self.player_c_v.vel.x += self.player_cfg['input_velocity']
                   
            elif action.phase == CommandPhase.END:
                    self.player_c_v.vel.x -= self.player_cfg['input_velocity']