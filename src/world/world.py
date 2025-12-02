from typing import List, Sequence, Type, TYPE_CHECKING
if TYPE_CHECKING:
    from .entity import Entity
    from graphics import MessageLog
from .tiles import TileMap, Tile
from .spatial_hash import SpatialHash


class World:
    def __init__(self, message_log: MessageLog):
        self.tile_map = TileMap()
        self.spatial_hash = SpatialHash(cell_size=1.0)  # 1 world unit per cell
        self.log = message_log

    def add_entity(self, entity: Entity):
        self.spatial_hash.insert(entity)

    def remove_entity(self, entity: Entity):
        """Remove an entity from the world."""
        self.spatial_hash.remove(entity)

    def update_entity_position(self, entity: Entity):
        """Update an entity's position in the spatial hash. Call after entity movement."""
        self.spatial_hash.update(entity)

    def get_entities_in_region(self, min_x: float, min_y: float, max_x: float, max_y: float) -> List[Entity]:
        """Get all entities that may be visible in the given world coordinate region."""
        return self.spatial_hash.query_region(min_x, min_y, max_x, max_y)

    def get_tile_map(self) -> TileMap:
        return self.tile_map

    def get_entities(self) -> List[Entity]:
        return self.spatial_hash.get_all_entities()

    def get_tile_at(self, x: int, y: int) -> Tile | None:
        return self.tile_map.get_tile(x, y)

    def has_collision(self, source: Entity, excluded: Sequence[Type[Entity]] | None = None) -> Entity | None:
        """
        Check if the source entity collides with any other entity in the world,
        excluding entities of the specified types.

        Uses axis-aligned bounding box (AABB) collision detection.
        Uses spatial hash to only check nearby entities.
        """
        # Query entities in the region the source occupies
        nearby = self.spatial_hash.query_region(
            source.x, source.y,
            source.x + source.world_units_width,
            source.y + source.world_units_height
        )
        
        for entity in nearby:
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
        Uses spatial hash to only check nearby entities.
        """
        nearby = self.spatial_hash.query_point(x, y)
        
        for entity in nearby:
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
        """Return a list of entities within the specified radius from point (x, y).
        
        Uses spatial hash to only check entities in the bounding region.
        """
        # Query the square region that bounds the circle
        nearby = self.spatial_hash.query_region(
            x - radius, y - radius,
            x + radius, y + radius
        )
        
        result = []
        for entity in nearby:
            if excluded and isinstance(entity, tuple(excluded)):
                continue
            dist = self.distance_between(x, y, entity.x + entity.world_units_width / 2, entity.y + entity.world_units_height / 2)
            if dist <= radius:
                result.append(entity)
        return result