import pygame

from src.create.prefab_creator import create_sprite
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_blinking import CBlinking
from src.ecs.systems.s_blinking_text import system_blinking_text
from src.ecs.systems.s_moving_text import system_moving_text
from src.engine.scenes.scene import Scene
from src.ecs.components.c_input_command import CInputCommand
from src.engine.service_locator import ServiceLocator 

class MenuScene(Scene):
    def do_create(self):
        self._interface_cfg = ServiceLocator.configurations_service.get("assets/cfg/menu_screen.json")
        self._window_cfg = ServiceLocator.configurations_service.get("assets/cfg/window.json")
        screen_height = self._window_cfg["size"]["h"]

        create_text(self.ecs_world, self._interface_cfg["1up"]["text"], 
                    self._interface_cfg["start"]["size"],  
                    pygame.Color(self._interface_cfg["1up"]["color"]["r"], 
                                 self._interface_cfg["1up"]["color"]["g"], 
                                 self._interface_cfg["1up"]["color"]["b"]), 
                    pygame.Vector2(self._interface_cfg["1up"]["position"]["x"], 
                                    self._interface_cfg["1up"]["position"]["y"] + screen_height), 
                    TextAlignment.CENTER)
        create_text(self.ecs_world, self._interface_cfg["score"]["text"], 
                    self._interface_cfg["score"]["size"],  
                    pygame.Color(self._interface_cfg["score"]["color"]["r"], 
                                 self._interface_cfg["score"]["color"]["g"], 
                                 self._interface_cfg["score"]["color"]["b"]), 
                    pygame.Vector2(self._interface_cfg["score"]["position"]["x"], 
                                    self._interface_cfg["score"]["position"]["y"] + screen_height), 
                    TextAlignment.CENTER)
        create_text(self.ecs_world, self._interface_cfg["hi_score"]["text"], 
                    self._interface_cfg["start"]["size"],  
                    pygame.Color(self._interface_cfg["hi_score"]["color"]["r"], 
                                 self._interface_cfg["hi_score"]["color"]["g"], 
                                 self._interface_cfg["hi_score"]["color"]["b"]), 
                    pygame.Vector2(self._interface_cfg["hi_score"]["position"]["x"], 
                                    self._interface_cfg["hi_score"]["position"]["y"] + screen_height), 
                    TextAlignment.CENTER)
        create_text(self.ecs_world, self._interface_cfg["hi_score_value"]["text"], 
                    self._interface_cfg["start"]["size"],  
                    pygame.Color(self._interface_cfg["hi_score_value"]["color"]["r"], 
                                 self._interface_cfg["hi_score_value"]["color"]["g"], 
                                 self._interface_cfg["hi_score_value"]["color"]["b"]), 
                    pygame.Vector2(self._interface_cfg["hi_score_value"]["position"]["x"], 
                                    self._interface_cfg["hi_score_value"]["position"]["y"] + screen_height), 
                    TextAlignment.CENTER)
        create_text(self.ecs_world, self._interface_cfg["start"]["text"], 
                    self._interface_cfg["start"]["size"], 
                    pygame.Color(self._interface_cfg["start"]["color"]["r"], 
                                 self._interface_cfg["start"]["color"]["g"], 
                                 self._interface_cfg["start"]["color"]["b"]), 
                    pygame.Vector2(self._interface_cfg["start"]["position"]["x"], 
                                    self._interface_cfg["start"]["position"]["y"] + screen_height), 
                    TextAlignment.CENTER, isBlinking=True)
        
        surface = ServiceLocator.images_service.get(self._interface_cfg["logo"]["image"])
        position = pygame.Vector2(self._interface_cfg["logo"]["position"]["x"] - surface.get_size()[0] / 2, 
                                  self._interface_cfg["logo"]["position"]["y"] + screen_height)
        velocity = pygame.Vector2(0,0)
        create_sprite( self.ecs_world, position, velocity, surface)
        
        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action,
                                     CInputCommand("START_GAME", pygame.K_z))

    def do_action(self, action: CInputCommand):
        if action.name == "START_GAME":
            self.switch_scene("START_SCENE")

    def do_update(self, delta_time: float):
        system_moving_text(self.ecs_world, delta_time)
        system_blinking_text(self.ecs_world, delta_time)
