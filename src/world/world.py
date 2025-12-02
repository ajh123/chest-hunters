from typing import List, Sequence, Type, TYPE_CHECKING
if TYPE_CHECKING:
    from .entity import Entity
from .tiles import TileMap, Tile


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

    def has_collision(self, source: Entity, excluded: Sequence[Type[Entity]] | None = None) -> Entity | None:
        """
        Check if the source entity collides with any other entity in the world,
        excluding entities of the specified types.

        Uses axis-aligned bounding box (AABB) collision detection.
        """
        for entity in self.get_entities():
            if entity is source:
                continue
            if excluded and isinstance(entity, tuple(excluded)):
                continue

            if (source.x < entity.x + entity.world_units_width and
                source.x + source.world_units_width > entity.x and
                source.y < entity.y + entity.world_units_height and
                source.y + source.world_units_height > entity.y):
                return entity
        return None
    
    def point_collision(self, x: float, y: float, excluded: Sequence[Type[Entity]] | None = None) -> Entity | None:
        """
        Check if the point (x, y) collides with any entity in the world,
        excluding entities of the specified types.

        Uses axis-aligned bounding box (AABB) collision detection.
        """
        for entity in self.get_entities():
            if excluded and isinstance(entity, tuple(excluded)):
                continue

            if (x >= entity.x and
                x <= entity.x + entity.world_units_width and
                y >= entity.y and
                y <= entity.y + entity.world_units_height):
                return entity
        return None

    def distance_between(self, sx: float, sy: float, ex: float, ey: float) -> float:
        """Calculate Euclidean distance between two points."""
        return ((sx - ex) ** 2 + (sy - ey) ** 2) ** 0.5
    
    def entities_in_radius(self, x: float, y: float, radius: float, excluded: Sequence[Type[Entity]] | None = None) -> List[Entity]:
        """Return a list of entities within the specified radius from point (x, y)."""
        result = []
        for entity in self.get_entities():
            if excluded and isinstance(entity, tuple(excluded)):
                continue
            dist = self.distance_between(x, y, entity.x + entity.world_units_width / 2, entity.y + entity.world_units_height / 2)
            if dist <= radius:
                result.append(entity)
        return result