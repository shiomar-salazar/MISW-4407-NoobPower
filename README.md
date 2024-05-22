# MISW-4407-NoobPower
Espacio de Trabajo del Equipo Noob Power para la Materia MISW-4407: Introduccion al Desarrollo de Video Juegos

## Integrantes:

|   Nombre                         |   Correo                      | Codigo    |
|----------------------------------|-------------------------------|-----------|
| Sara Giselle Ramírez Pimiento    | sg.ramirez940@uniandes.edu.co | 201112368 |
| Juan David Salguero              | j.salguero@uniandes.edu.co    | 201923136 |
| Nicolás Rey                      | n.reyd@uniandes.edu.co        | 202317668 |
| Shiomar Alberto Salazar Castillo | s.salazarc@uniandes.edu.co    | 202213359 |

## Diagrama de actual del proyecto
> Imagen generada con plantUML

<img src="https://github.com/shiomar-salazar/MISW-4407-NoobPower/blob/main/Documentation/digram.png">

## Contorles del Juego
- `Flechas direcionales`: Para mover al Jugador de Izquierda a Derecha.
- `Tecla Z`: Boton de Funcion:
  - Para Iniciar el Juego.
  - Para disparar proyectil.
- `Tecla G`: Para funcionalidad Extra, God Mode.
  - En este modo sale un texto en verde anunciando el modo.
  - La balas de los enemigo no hacen daño al jugador.
- `Barra Espaciadora`: Vista de Debug:
  - Se activa la vista de debug de rectangulos.
  - Se muestra los puntos de origen de las entidades dibujadas y sus superficies.
  - No se muestra texto, por exceso de informacion que lo hace ilegible.
  - Se utilizo para debiggear las animaciones de las explociones.

## Estructura del Proyecto
```
MISW-4407-NoobPower
├─ .git
├─ .gitignore
├─ .pylintrc
├─ .vscode
│  ├─ launch.json
│  └─ settings.json
├─ assets
│  ├─ cfg
│  │  ├─ bullet.json
│  │  ├─ enemies.json
│  │  ├─ enemy_field.json
│  │  ├─ explosion.json
│  │  ├─ game_over.json
│  │  ├─ interface.json
│  │  ├─ menu_screen.json
│  │  ├─ pause.json
│  │  ├─ player.json
│  │  ├─ starfield.json
│  │  ├─ start_screen.json
│  │  └─ window.json
│  ├─ fnt
│  │  └─ PressStart2P.ttf
│  ├─ img
│  │  ├─ invaders_char.png
│  │  ├─ invaders_enemy_01.png
│  │  ├─ invaders_enemy_02.png
│  │  ├─ invaders_enemy_03.png
│  │  ├─ invaders_enemy_04.png
│  │  ├─ invaders_enemy_explosion.png
│  │  ├─ invaders_level_flag.png
│  │  ├─ invaders_life.png
│  │  ├─ invaders_logo_title.png
│  │  └─ invaders_player_explosion.png
│  └─ snd
│     ├─ enemy_die.ogg
│     ├─ enemy_launch.ogg
│     ├─ game_loop.ogg
│     ├─ game_over.ogg
│     ├─ game_paused.ogg
│     ├─ game_start.ogg
│     ├─ player_die.ogg
│     └─ player_shoot.ogg
├─ Documentation
│  ├─ digram.png
│  └─ digram.puml
├─ esper
│  ├─ py.typed
│  └─ __init__.py
├─ main.py
├─ README.md
├─ requirements.txt
└─ src
   ├─ create
   │  ├─ prefab_creator.py
   │  ├─ prefab_creator_interface.py
   │  ├─ prefab_general.py
   │  └─ __init__.py
   ├─ ecs
   │  ├─ components
   │  │  ├─ c_animation.py
   │  │  ├─ c_blinking.py
   │  │  ├─ c_input_command.py
   │  │  ├─ c_reload.py
   │  │  ├─ c_surface.py
   │  │  ├─ c_transform.py
   │  │  ├─ c_velocity.py
   │  │  ├─ tags
   │  │  │  ├─ c_tag_bullet.py
   │  │  │  ├─ c_tag_enemy.py
   │  │  │  ├─ c_tag_enemy_bullet.py
   │  │  │  ├─ c_tag_explosion.py
   │  │  │  ├─ c_tag_player.py
   │  │  │  ├─ c_tag_player_bullet.py
   │  │  │  └─ c_tag_star.py
   │  │  └─ __init__.py
   │  ├─ systems
   │  │  ├─ s_animation.py
   │  │  ├─ s_blinking_text.py
   │  │  ├─ s_bullet_player_align.py
   │  │  ├─ s_bullet_shoot.py
   │  │  ├─ s_collision_enemy_bullet.py
   │  │  ├─ s_collision_player_bullet.py
   │  │  ├─ s_enemy_block_movement.py
   │  │  ├─ s_enemy_fire.py
   │  │  ├─ s_explosion_kill.py
   │  │  ├─ s_input.py
   │  │  ├─ s_movement.py
   │  │  ├─ s_moving_text.py
   │  │  ├─ s_player_limits.py
   │  │  ├─ s_rendering.py
   │  │  ├─ s_rendering_debug_rects.py
   │  │  ├─ s_screen_bullet.py
   │  │  ├─ s_starfield.py
   │  │  ├─ s_toggle_god_mode.py
   │  │  └─ __init__.py
   │  └─ __init__.py
   ├─ engine
   │  ├─ game_engine.py
   │  ├─ scenes
   │  │  ├─ scene.py
   │  │  └─ __init__.py
   │  ├─ services
   │  │  ├─ cfgs_service.py
   │  │  ├─ fonts_service.py
   │  │  ├─ images_service.py
   │  │  ├─ sounds_service.py
   │  │  └─ __init__.py
   │  ├─ service_locator.py
   │  └─ __init__.py
   ├─ game
   │  ├─ menu_scene.py
   │  ├─ play_scene.py
   │  ├─ start_scene.py
   │  └─ __init__.py
   └─ __init__.py

```