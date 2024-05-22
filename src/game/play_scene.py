from enum import Enum
import pygame

import src
from src.create.prefab_creator import create_level, create_player
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_blinking_text import system_blinking_text
from src.ecs.systems.s_bullet_player_align import system_bullet_player_align
from src.ecs.systems.s_bullet_shoot import system_bullet_shoot
from src.ecs.systems.s_collision_enemy_bullet import system_collision_enemy_bullet
from src.ecs.systems.s_collision_player_bullet import system_collision_player_bullet
from src.ecs.systems.s_enemy_block_movement import system_enemy_block_movement
from src.ecs.systems.s_enemy_fire import system_enemy_fire
from src.ecs.systems.s_explosion_kill import system_explosion_kill
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_limits import system_player_limits
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_rendering_debug_rects import system_rendering_debug_rects
from src.ecs.systems.s_screen_bullet import system_screen_bullet
from src.ecs.systems.s_toggle_god_mode import system_toggle_god_mode
from src.engine.scenes.scene import Scene
from src.engine.service_locator import ServiceLocator

class DebugView(Enum):
    NONE = 0
    RECTS = 1


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
        self._interface_cfg = ServiceLocator.configurations_service.get("assets/cfg/start_screen.json")
        self.game_over_cfg = ServiceLocator.configurations_service.get("assets/cfg/game_over.json")
        self._screen_surf = screen_surf
        self.is_paused = False
        self.pause_text = None
        self.score = 0
        self.score_text = None 
        self._debug_view = DebugView.NONE
        self.life_text = None
        self.lifes = self.player_cfg["vidas"]
        self.level_text = None
        self.level = 1
        self.god_text = None

    def do_create(self):
        self.level_text = create_text(self.ecs_world, str(self.level), 
                    self._interface_cfg["Level"]["size"],  
                    pygame.Color(255,255,255), 
                    pygame.Vector2(self._interface_cfg["Level"]["position"]["x"], 
                                    self._interface_cfg["Level"]["position"]["y"] + 10), 
                    TextAlignment.CENTER)
        self.player_entity = create_player(self.ecs_world, self.player_cfg, self._screen_surf)
        self.player_c_v = self.ecs_world.component_for_entity(self.player_entity, CVelocity)
        self.player_c_t = self.ecs_world.component_for_entity(self.player_entity, CTransform)
        self.player_c_s = self.ecs_world.component_for_entity(self.player_entity, CSurface)
        create_text(self.ecs_world, self._interface_cfg["1up"]["text"], 
                    self._interface_cfg["1up"]["size"],  
                    pygame.Color(self._interface_cfg["1up"]["color"]["r"], 
                                 self._interface_cfg["1up"]["color"]["g"], 
                                 self._interface_cfg["1up"]["color"]["b"]), 
                    pygame.Vector2(self._interface_cfg["1up"]["position"]["x"], 
                                    self._interface_cfg["1up"]["position"]["y"]), 
                    TextAlignment.CENTER)
        self.score_text = create_text(self.ecs_world, self._interface_cfg["score"]["text"], 
                    self._interface_cfg["score"]["size"],  
                    pygame.Color(self._interface_cfg["score"]["color"]["r"], 
                                 self._interface_cfg["score"]["color"]["g"], 
                                 self._interface_cfg["score"]["color"]["b"]), 
                    pygame.Vector2(self._interface_cfg["score"]["position"]["x"], 
                                    self._interface_cfg["score"]["position"]["y"]), 
                    TextAlignment.CENTER)
        create_text(self.ecs_world, self._interface_cfg["hi_score"]["text"], 
                    self._interface_cfg["hi_score"]["size"],  
                    pygame.Color(self._interface_cfg["hi_score"]["color"]["r"], 
                                 self._interface_cfg["hi_score"]["color"]["g"], 
                                 self._interface_cfg["hi_score"]["color"]["b"]), 
                    pygame.Vector2(self._interface_cfg["hi_score"]["position"]["x"], 
                                    self._interface_cfg["hi_score"]["position"]["y"]), 
                    TextAlignment.CENTER)
        create_text(self.ecs_world, self._interface_cfg["hi_score_value"]["text"], 
                    self._interface_cfg["hi_score_value"]["size"],  
                    pygame.Color(self._interface_cfg["hi_score_value"]["color"]["r"], 
                                 self._interface_cfg["hi_score_value"]["color"]["g"], 
                                 self._interface_cfg["hi_score_value"]["color"]["b"]), 
                    pygame.Vector2(self._interface_cfg["hi_score_value"]["position"]["x"], 
                                    self._interface_cfg["hi_score_value"]["position"]["y"]), 
                    TextAlignment.CENTER)
        create_text(self.ecs_world, self._interface_cfg["Lifes"]["text"],
                    self._interface_cfg["Lifes"]["size"],  
                    pygame.Color(self._interface_cfg["Lifes"]["color"]["r"], 
                                 self._interface_cfg["Lifes"]["color"]["g"], 
                                 self._interface_cfg["Lifes"]["color"]["b"]), 
                    pygame.Vector2(self._interface_cfg["Lifes"]["position"]["x"], 
                                    self._interface_cfg["Lifes"]["position"]["y"]), 
                    TextAlignment.CENTER)
        self.life_text = create_text(self.ecs_world, str(self.lifes),
                    self._interface_cfg["Lifes"]["size"],  
                    pygame.Color(255,255,255), 
                    pygame.Vector2(self._interface_cfg["Lifes"]["position"]["x"], 
                                    self._interface_cfg["Lifes"]["position"]["y"] + 10), 
                    TextAlignment.CENTER)
        create_text(self.ecs_world, self._interface_cfg["Level"]["text"],
                    self._interface_cfg["Level"]["size"],  
                    pygame.Color(self._interface_cfg["Level"]["color"]["r"], 
                                 self._interface_cfg["Level"]["color"]["g"], 
                                 self._interface_cfg["Level"]["color"]["b"]), 
                    pygame.Vector2(self._interface_cfg["Level"]["position"]["x"], 
                                    self._interface_cfg["Level"]["position"]["y"]), 
                    TextAlignment.CENTER)
        create_level(self.ecs_world, self.enemies_cfg, self.level_cfg, self.window_cfg)

    def do_update(self, delta_time: float): 
        if not self.is_paused:
            if self.lifes != 0:
                system_enemy_fire(self.ecs_world, delta_time, self.bullet_cfg)
            system_movement(self.ecs_world, delta_time)
            system_enemy_block_movement(self.ecs_world, delta_time, self.window_cfg["size"]["w"])
            system_screen_bullet(self.ecs_world, self._screen_surf)
            system_player_limits(self.ecs_world, self._screen_surf)

            #actualización de puntaje cuando se destruye un enemigo
            new_score, reset = system_collision_enemy_bullet(self.ecs_world, self.explosion_cfg["enemy_explosion"])
            self.score += new_score
            if self.score_text is not None:
                self.ecs_world.delete_entity(self.score_text)
            self.score_text = create_text(self.ecs_world, str(self.score), 
                    self._interface_cfg["score"]["size"],  
                    pygame.Color(self._interface_cfg["score"]["color"]["r"], 
                                self._interface_cfg["score"]["color"]["g"], 
                                self._interface_cfg["score"]["color"]["b"]), 
                    pygame.Vector2(self._interface_cfg["score"]["position"]["x"], 
                                    self._interface_cfg["score"]["position"]["y"]), 
                    TextAlignment.CENTER)

            #Colisiones entre el jugador y las balas enemigas, si el jugador muere se crea una nueva instancia
            dead = system_collision_player_bullet(self.ecs_world, self.explosion_cfg["player_explosion"], delta_time, self._screen_surf)
            if dead:
                self.lifes -= 1
                if self.life_text is not None:
                    self.ecs_world.delete_entity(self.life_text)
                self.life_text = create_text(self.ecs_world, str(self.lifes),
                                            self._interface_cfg["Lifes"]["size"],  
                                            pygame.Color(255,255,255), 
                                            pygame.Vector2(self._interface_cfg["Lifes"]["position"]["x"], 
                                                            self._interface_cfg["Lifes"]["position"]["y"] + 10), 
                                            TextAlignment.CENTER)
                if self.lifes == 0:
                    ServiceLocator.sounds_service.play(self.game_over_cfg["sound"])
                    create_text(self.ecs_world, self.game_over_cfg["text"], self.game_over_cfg["size"], 
                                pygame.Color(self.game_over_cfg["color"]["r"],self.game_over_cfg["color"]["g"],self.game_over_cfg["color"]["b"]), 
                                pygame.Vector2(self.game_over_cfg["position"]["x"], self.game_over_cfg["position"]["y"]), 
                                TextAlignment.CENTER, True)
                    self.ecs_world.delete_entity(self.player_entity)
                    return
                else:
                    create_text(self.ecs_world,"READY",7,pygame.Color(255,0,0),pygame.Vector2(128,120),TextAlignment.CENTER, True)
            system_explosion_kill(self.ecs_world)
            system_bullet_player_align(self.ecs_world, self.bullet_cfg)
            system_animation(self.ecs_world, delta_time)
            system_blinking_text(self.ecs_world, delta_time)
            if reset:
                self.level += 1
                self._game_engine.switch_scene("PLAY_GAME")
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
        if action.name == "RESTART_GAME" and action.phase == CommandPhase.START:
            if self.lifes == 0:
                self.lifes = self.player_cfg["vidas"]
                self.score = 0
                self._game_engine.switch_scene("MENU_SCENE")
                
        if action.name == "TOGGLE_DEBUG_VIEW" and action.phase == CommandPhase.START:
            if self._debug_view == DebugView.NONE:
                self._debug_view = DebugView.RECTS
            else:
                self._debug_view = DebugView.NONE

        if action.name == "GOD_MODE" and action.phase == CommandPhase.START:
            if system_toggle_god_mode(self.ecs_world):
                self.god_text = create_text(self.ecs_world, "God Mode", 7,
                                                pygame.Color(0,255,0),
                                                pygame.Vector2(30,230),
                                                TextAlignment.CENTER,True)
            else:
                if self.god_text != None:
                    self.ecs_world.delete_entity(self.god_text)
                

    def do_draw(self, screen):
        # Evaluar vistas de depurado y vistas normales
        if self._debug_view == DebugView.RECTS:
            system_rendering_debug_rects(self.ecs_world, screen)
        else:
            system_rendering(self.ecs_world, screen)

    def do_clean(self):
        self._debug_view = DebugView.NONE
        self._paused = False

                
