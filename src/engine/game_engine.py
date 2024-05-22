import asyncio
import pygame

import esper
from src.create.prefab_general import create_stars
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_starfield import system_starfield
from src.engine.scenes.scene import Scene
from src.engine.service_locator import ServiceLocator
from src.game.menu_scene import MenuScene
from src.game.play_scene import PlayScene
from src.game.start_scene import StartScene

class GameEngine:
    def __init__(self) -> None:
        self._window_cfg = ServiceLocator.configurations_service.get("assets/cfg/window.json")
        self._starfield_cfg = ServiceLocator.configurations_service.get("assets/cfg/starfield.json")
        pygame.init()
        self.ecs_world = esper.World()
        pygame.display.set_caption(self._window_cfg["title"])
        self.screen = pygame.display.set_mode(
            (self._window_cfg["size"]["w"], self._window_cfg["size"]["h"]))

        self._clock = pygame.time.Clock()
        self._framerate = self._window_cfg["framerate"]
        self._delta_time = 0
        self._bg_color = pygame.Color(self._window_cfg["bg_color"]["r"],
                                     self._window_cfg["bg_color"]["g"],
                                     self._window_cfg["bg_color"]["b"])
        self.is_running = False

        self._scenes:dict[str, Scene] = {}
        self._scenes["MENU_SCENE"] = MenuScene(self)
        self._scenes["START_SCENE"] = StartScene(self)
        self._scenes["PLAY_GAME"] = PlayScene(engine=self, screen_surf=self.screen)
        self._current_scene:Scene = None
        self._scene_name_to_switch:str = None

    async def run(self, start_scene_name:str) -> None:
        self.is_running = True
        self._current_scene = self._scenes[start_scene_name]
        self._create()
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            self._handle_switch_scene()
            await asyncio.sleep(0)
        self._do_clean()

    def switch_scene(self, new_scene_name:str):
        self._scene_name_to_switch = new_scene_name
    
    def _create(self):
        create_stars(self.ecs_world, self._starfield_cfg, self._window_cfg)
        self._current_scene.do_create()

    def _calculate_time(self):
        self._clock.tick(self._framerate)
        self._delta_time = self._clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            self._current_scene.do_process_events(event)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_starfield(self.ecs_world, self._delta_time, self._starfield_cfg, self._window_cfg)
        self.ecs_world._clear_dead_entities()
        self._current_scene.simulate(self._delta_time)

    def _draw(self):
        self.screen.fill(self._bg_color)
        system_rendering(self.ecs_world, self.screen)        
        self._current_scene.do_draw(self.screen)
        pygame.display.flip()

    def _handle_switch_scene(self):
        if self._scene_name_to_switch is not None:
            self._current_scene.clean()
            self._current_scene = self._scenes[self._scene_name_to_switch]
            self._current_scene.do_create()
            self._scene_name_to_switch = None

    def _do_action(self, action:CInputCommand):        
        self._current_scene.do_action(action)

    def _do_clean(self):
        if self._current_scene is not None:
            self._current_scene.clean()
        pygame.quit()
        
