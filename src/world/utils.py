from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from .entity import Entity
    from .world import World
from constants import TILE_SIZE


def is_entity_at(world: 'World', x: int, y: int, excluded: List['Entity'] | None) -> 'Entity' | None:
    # Determine whether any non-excluded entity occupies the given tile
    # coordinates. Entities store their position as world (tile) coords
    # but their width/height are pixels, so convert size to tile coverage
    # before doing the AABB test.
    for entity in world.get_entities():
        # Any excluded entity should not be treated as occupying tiles.
        if excluded and entity in excluded:
            continue

        try:
            ex = float(entity.x)
            ey = float(entity.y)
            ew = float(entity.width)
            eh = float(entity.height)
        except Exception:
            continue

        tiles_w = max(1.0, ew / TILE_SIZE)
        tiles_h = max(1.0, eh / TILE_SIZE)

        if (ex <= x < ex + tiles_w) and (ey <= y < ey + tiles_h):
            return entity

    return None