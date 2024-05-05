import asyncio
import json
import random
import time
import pygame
import esper

from src.create.prefab_creator import create_bullet, create_input_player, create_level, create_player, create_stars
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_collision_enemy_bullet import system_collision_enemy_bullet
from src.ecs.systems.s_enemy_block_movement import system_enemy_block_movement
from src.ecs.systems.s_explosion_kill import system_explosion_kill
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_limits import system_player_limits
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.ecs.systems.s_screen_bullet import system_screen_bullet
from src.ecs.systems.s_starfield import system_starfield

class GameEngine:
    def __init__(self) -> None:
        self._load_config_files()

        pygame.init()
        pygame.display.set_caption(self.window_cfg["title"])
        self.screen = pygame.display.set_mode(
            (self.window_cfg["size"]["w"], self.window_cfg["size"]["h"]), 
            pygame.SCALED)

        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window_cfg["framerate"]
        self.delta_time = 0
        self.bg_color = pygame.Color(self.window_cfg["bg_color"]["r"],
                                     self.window_cfg["bg_color"]["g"],
                                     self.window_cfg["bg_color"]["b"])
        self.ecs_world = esper.World()

    def _load_config_files(self):
        with open("assets/cfg/window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open("assets/cfg/enemies.json", encoding="utf-8") as enemy_file:
            self.enemies_cfg = json.load(enemy_file)
        with open("assets/cfg/enemy_field.json", encoding="utf-8") as enemy_field:
            self.level_cfg = json.load(enemy_field)
        with open("assets/cfg/bullet.json", encoding="utf-8") as bullet_file:
            self.bullet_cfg = json.load(bullet_file)
        with open("assets/cfg/player.json", encoding="utf-8") as player_file:
            self.player_cfg = json.load(player_file)
        with open("assets/cfg/explosion.json", encoding="utf-8") as explosion_file:
            self.explosion_cfg = json.load(explosion_file)
        with open("assets/cfg/starfield.json", encoding="utf-8") as starfield_file:
            self.starfield_cfg = json.load(starfield_file)

    async def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            await asyncio.sleep(0)
        self._clean()

    def _create(self):
        self.player_entity = create_player(self.ecs_world, self.player_cfg, self.screen)
        self.player_c_v = self.ecs_world.component_for_entity(self.player_entity, CVelocity)
        self.player_c_t = self.ecs_world.component_for_entity(self.player_entity, CTransform)
        self.player_c_s = self.ecs_world.component_for_entity(self.player_entity, CSurface)
        create_level(self.ecs_world, self.enemies_cfg, self.level_cfg, self.window_cfg)
        create_input_player(self.ecs_world)
        create_stars(self.ecs_world, self.starfield_cfg, self.window_cfg)

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0
    
    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_starfield(self.ecs_world, self.delta_time, self.starfield_cfg, self.window_cfg)
        system_movement(self.ecs_world, self.delta_time)
        system_enemy_block_movement(self.ecs_world, self.delta_time, self.window_cfg["size"]["w"])
        system_screen_bullet(self.ecs_world, self.screen)
        system_player_limits(self.ecs_world, self.screen)
        system_screen_bounce(self.ecs_world, self.screen)
        system_collision_enemy_bullet(self.ecs_world, self.explosion_cfg["enemy_explosion"])
        system_explosion_kill(self.ecs_world)
        system_animation(self.ecs_world, self.delta_time)

        self.ecs_world._clear_dead_entities()
        self.player_bullets = len(self.ecs_world.get_component(CTagPlayerBullet))

    def _draw(self):
        self.screen.fill(self.bg_color)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()

    def _do_action(self, c_input: CInputCommand):
        if c_input.name == "PLAYER_FIRE" and c_input.phase == CommandPhase.START and self.player_bullets == 0:
            #TODO: Shiomar -> Agregar datos de player (Pos y Size)
            create_bullet(self.ecs_world, self.player_c_t.pos,
                          self.player_c_s.area.size, self.bullet_cfg)
        #Input de movimiento del jugador
        elif c_input.name == 'PLAYER_LEFT':
            if c_input.phase == CommandPhase.START:
                self.player_c_v.vel.x -= self.player_cfg['input_velocity']
                
            elif c_input.phase == CommandPhase.END:
                self.player_c_v.vel.x += self.player_cfg['input_velocity']

        elif c_input.name == 'PLAYER_RIGHT':
            if c_input.phase == CommandPhase.START:
                    self.player_c_v.vel.x += self.player_cfg['input_velocity']
                   
            elif c_input.phase == CommandPhase.END:
                    self.player_c_v.vel.x -= self.player_cfg['input_velocity']

    


