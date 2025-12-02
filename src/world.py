from typing import List
from entity import Entity
from tiles import TileMap, Tile
from camera import Camera
from constants import TILE_SIZE


class World:
    def __init__(self):
        self.tile_map = TileMap()
        self.entities: List[Entity] = []

    def add_entity(self, entity: Entity):
        self.entities.append(entity)

    def get_tile_map(self) -> TileMap:
        return self.tile_map

    def get_entities(self) -> List[Entity]:
        return self.entities

    def get_tile_at(self, x: int, y: int) -> Tile | None:
        return self.tile_map.get_tile(x, y)
    
    def is_entity_at(self, x: int, y: int) -> Entity | None:
        # Determine whether any non-camera entity occupies the given tile
        # coordinates. Entities store their position as world (tile) coords
        # but their width/height are pixels, so convert size to tile coverage
        # before doing the AABB test.
        for entity in self.entities:
            # The camera should not be treated as occupying tiles.
            if isinstance(entity, Camera):
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