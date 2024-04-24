# MISW-4407-NoobPower
Espacio de Trabajo del Equipo Noob Power para la Materia MISW-4407: Introduccion al Desarrollo de Video Juegos

## Integrantes:

|   Nombre                         |   Correo                      |
|----------------------------------|-------------------------------|
| Sara Giselle Ramírez Pimiento    | sg.ramirez940@uniandes.edu.co |
| Juan David Salguero              | j.salguero@uniandes.edu.co    |
| Nicolás Rey                      | n.reyd@uniandes.edu.co        |
| Shiomar Alberto Salazar Castillo | s.salazarc@uniandes.edu.co    |

## Estructura del Proyecto
```
MISW-4407-NoobPower
├─ .pylintrc
├─ .vscode
│  ├─ launch.json
│  └─ settings.json
├─ assets
│  ├─ cfg
│  │  ├─ interface.json
│  │  ├─ starfield.json
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
├─ build
├─ esper
│  ├─ py.typed
│  └─ __init__.py
├─ main.py
├─ README.md
├─ requirements.txt
└─ src
   ├─ create
   │  ├─ prefab_creator.py
   │  └─ __init__.py
   ├─ ecs
   │  ├─ components
   │  │  ├─ c_surface.py
   │  │  ├─ c_transform.py
   │  │  ├─ c_velocity.py
   │  │  └─ __init__.py
   │  ├─ systems
   │  │  ├─ s_movement.py
   │  │  ├─ s_rendering.py
   │  │  ├─ s_screen_bounce.py
   │  │  └─ __init__.py
   │  └─ __init__.py
   ├─ engine
   │  ├─ game_engine.py
   │  └─ __init__.py
   └─ __init__.py
```