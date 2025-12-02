from typing import List
from entity import Entity
from tiles import TileMap, Tile

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
        for entity in self.entities:
            if (entity.x <= x < entity.x + entity.width and
                entity.y <= y < entity.y + entity.height):
                return entity
        return None