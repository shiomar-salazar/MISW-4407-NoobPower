import json

import pygame

import src
from src.create.prefab_creator import create_input_player, create_level, create_player
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_bullet_player_align import system_bullet_player_align
from src.ecs.systems.s_bullet_shoot import system_bullet_shoot
from src.ecs.systems.s_collision_enemy_bullet import system_collision_enemy_bullet
from src.ecs.systems.s_collision_player_bullet import system_collision_player_bullet
from src.ecs.systems.s_enemy_block_movement import system_enemy_block_movement
from src.ecs.systems.s_enemy_fire import system_enemy_fire
from src.ecs.systems.s_explosion_kill import system_explosion_kill
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_limits import system_player_limits
from src.ecs.systems.s_score import system_score
from src.ecs.systems.s_screen_bullet import system_screen_bullet
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
        self.pause_cfg = ServiceLocator.configurations_service.get("assets/cfg/pause.json")
        self._screen_surf = screen_surf
        self.is_paused = False
        self.pause_text = None

    def do_create(self):
        self._interface_cfg = ServiceLocator.configurations_service.get("assets/cfg/start_screen.json")
        self.player_entity = create_player(self.ecs_world, self.player_cfg, self._screen_surf)
        self.player_c_v = self.ecs_world.component_for_entity(self.player_entity, CVelocity)
        self.player_c_t = self.ecs_world.component_for_entity(self.player_entity, CTransform)
        self.player_c_s = self.ecs_world.component_for_entity(self.player_entity, CSurface)
        create_text(self.ecs_world, self._interface_cfg["00"]["text"], 
                    self._interface_cfg["00"]["size"],  
                    pygame.Color(self._interface_cfg["00"]["color"]["r"], 
                                 self._interface_cfg["00"]["color"]["g"], 
                                 self._interface_cfg["00"]["color"]["b"]), 
                    pygame.Vector2(self._interface_cfg["00"]["position"]["x"], 
                                    self._interface_cfg["00"]["position"]["y"]), 
                    TextAlignment.CENTER)
        create_level(self.ecs_world, self.enemies_cfg, self.level_cfg, self.window_cfg)
        create_input_player(self.ecs_world)

    def do_update(self, delta_time: float): 
        if not self.is_paused:
            system_movement(self.ecs_world, delta_time)
            system_score(self.ecs_world)
            system_enemy_block_movement(self.ecs_world, delta_time, self.window_cfg["size"]["w"])
            system_enemy_fire(self.ecs_world, delta_time, self.bullet_cfg)
            system_screen_bullet(self.ecs_world, self._screen_surf)
            system_player_limits(self.ecs_world, self._screen_surf)
            system_collision_enemy_bullet(self.ecs_world, self.explosion_cfg["enemy_explosion"])

            #Colisiones entre el jugador y las balas enemigas, si el jugador muere se crea una nueva instancia
            dead = system_collision_player_bullet(self.ecs_world, self.explosion_cfg["player_explosion"], self.player_cfg, self._screen_surf)
            if dead:
                self.player_entity = create_player(self.ecs_world, self.player_cfg, self._screen_surf)
                self.player_c_v = self.ecs_world.component_for_entity(self.player_entity, CVelocity)
                self.player_c_t = self.ecs_world.component_for_entity(self.player_entity, CTransform)
                self.player_c_s = self.ecs_world.component_for_entity(self.player_entity, CSurface)
                create_input_player(self.ecs_world)
                dead = False

            system_explosion_kill(self.ecs_world)
            system_bullet_player_align(self.ecs_world, self.bullet_cfg)
            system_animation(self.ecs_world, delta_time)
            self.ecs_world._clear_dead_entities()
        
    def do_action(self, action: CInputCommand):
        if action.name == "PLAYER_FIRE" and action.phase == CommandPhase.START:
            system_bullet_shoot(self.ecs_world, self.bullet_cfg)
        #Input de movimiento del jugador
        if action.name == 'PLAYER_LEFT':
            if action.phase == CommandPhase.START:
                self.player_c_v.vel.x -= self.player_cfg['input_velocity']
                
            elif action.phase == CommandPhase.END:
                self.player_c_v.vel.x += self.player_cfg['input_velocity']

        elif action.name == 'PLAYER_RIGHT':
            if action.phase == CommandPhase.START:
                    self.player_c_v.vel.x += self.player_cfg['input_velocity']

            elif action.phase == CommandPhase.END:
                    self.player_c_v.vel.x -= self.player_cfg['input_velocity']
        if action.name == 'PAUSE':
            if self.is_paused and action.phase == CommandPhase.INACTIVE:
                self.is_paused = False
                self.ecs_world.delete_entity(self.pause_text)
                self.ecs_world.delete_entity(self.support_text)
            elif (not self.is_paused) and action.phase == CommandPhase.ACTIVE:
                self.is_paused = True
                self.pause_text = create_text(self.ecs_world, self.pause_cfg["PAUSE"]["text"], 
                                              self.pause_cfg["PAUSE"]["size"],
                                              pygame.Color(self.pause_cfg["PAUSE"]["color"]["r"], 
                                                           self.pause_cfg["PAUSE"]["color"]["g"],
                                                           self.pause_cfg["PAUSE"]["color"]["b"]),
                                              pygame.Vector2(self._screen_surf.get_width() // 2, 
                                              self._screen_surf.get_height() // 2),
                                              TextAlignment.CENTER, isBlinking=True)
                self.support_text = create_text(self.ecs_world, self.pause_cfg["SUPPORT"]["text"],
                                                self.pause_cfg["SUPPORT"]["size"],
                                                pygame.Color(self.pause_cfg["SUPPORT"]["color"]["r"],
                                                self.pause_cfg["SUPPORT"]["color"]["g"],
                                                self.pause_cfg["SUPPORT"]["color"]["b"]),
                                                pygame.Vector2(self._screen_surf.get_width() // 2,
                                                self._screen_surf.get_height() // 2 + 10),
                                                TextAlignment.CENTER)

                
