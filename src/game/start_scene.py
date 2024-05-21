import pygame
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.engine.scenes.scene import Scene
from src.engine.service_locator import ServiceLocator


class StartScene(Scene):

    def do_create(self):
        self.start_time = None 
        self._interface_cfg = ServiceLocator.configurations_service.get("assets/cfg/start_screen.json")      

        create_text(self.ecs_world, self._interface_cfg["1up"]["text"], 
                    self._interface_cfg["1up"]["size"],  
                    pygame.Color(self._interface_cfg["1up"]["color"]["r"], 
                                 self._interface_cfg["1up"]["color"]["g"], 
                                 self._interface_cfg["1up"]["color"]["b"]), 
                    pygame.Vector2(self._interface_cfg["1up"]["position"]["x"], 
                                    self._interface_cfg["1up"]["position"]["y"]), 
                    TextAlignment.CENTER)
        create_text(self.ecs_world, self._interface_cfg["score"]["text"], 
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
        create_text(self.ecs_world, self._interface_cfg["game_start"]["text"], 
                    self._interface_cfg["game_start"]["size"], 
                    pygame.Color(self._interface_cfg["game_start"]["color"]["r"], 
                                 self._interface_cfg["game_start"]["color"]["g"], 
                                 self._interface_cfg["game_start"]["color"]["b"]), 
                    pygame.Vector2(self._interface_cfg["game_start"]["position"]["x"], 
                                    self._interface_cfg["game_start"]["position"]["y"]), 
                    TextAlignment.CENTER, isBlinking=True)
        create_text(self.ecs_world, self._interface_cfg["Lifes"]["text"],
                    self._interface_cfg["Lifes"]["size"],  
                    pygame.Color(self._interface_cfg["Lifes"]["color"]["r"], 
                                 self._interface_cfg["Lifes"]["color"]["g"], 
                                 self._interface_cfg["Lifes"]["color"]["b"]), 
                    pygame.Vector2(self._interface_cfg["Lifes"]["position"]["x"], 
                                    self._interface_cfg["Lifes"]["position"]["y"]), 
                    TextAlignment.CENTER)
        ServiceLocator.sounds_service.play(self._interface_cfg["sound"])
        self.start_time = pygame.time.get_ticks() 

    def do_update(self, delta_time: float):
        if self.start_time is not None and (pygame.time.get_ticks() - self.start_time > 3000):
            self.switch_scene("PLAY_GAME")
            self.start_time = None 
