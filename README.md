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
│  │  ├─ enemies.json
│  │  ├─ enemy_field.json
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
   │  └─ __init__.py
   ├─ ecs
   │  ├─ components
   │  │  ├─ c_animation.py
   │  │  ├─ c_surface.py
   │  │  ├─ c_transform.py
   │  │  ├─ c_velocity.py
   │  │  ├─ tags
   │  │  │  └─ c_tag_enemy.py
   │  │  └─ __init__.py
   │  ├─ systems
   │  │  ├─ s_animation.py
   │  │  ├─ s_movement.py
   │  │  ├─ s_rendering.py
   │  │  ├─ s_screen_bounce.py
   │  │  └─ __init__.py
   │  └─ __init__.py
   ├─ engine
   │  ├─ game_engine.py
   │  ├─ services
   │  │  └─ images_services.py
   │  ├─ service_locator.py
   │  └─ __init__.py
   └─ __init__.py

```