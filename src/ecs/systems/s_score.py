import esper
from src.ecs.components.c_score import CScore


def system_score(world: esper.World):
    score = 00
    components = world.get_components(CScore)
    for _, (c_score,) in components:
        score = c_score.score
    return score