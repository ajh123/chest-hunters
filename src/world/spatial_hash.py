from typing import TYPE_CHECKING, Set, Dict, Tuple, List
from collections import defaultdict

if TYPE_CHECKING:
    from .entity import Entity


class SpatialHash:
    """
    A spatial hash grid for efficient spatial queries.
    Entities are stored in cells based on their position.
    Cell size should match or be a multiple of your tile size for best performance.
    """
    
    def __init__(self, cell_size: float = 1.0):
        self.cell_size = cell_size
        self._grid: Dict[Tuple[int, int], Set[Entity]] = defaultdict(set)
        self._entity_cells: Dict[Entity, Set[Tuple[int, int]]] = defaultdict(set)

    def _get_cell(self, x: float, y: float) -> Tuple[int, int]:
        """Convert world coordinates to cell coordinates."""
        return (int(x // self.cell_size), int(y // self.cell_size))

    def _get_cells_for_entity(self, entity: 'Entity') -> Set[Tuple[int, int]]:
        """Get all cells that an entity occupies based on its bounding box."""
        min_cell_x, min_cell_y = self._get_cell(entity.x, entity.y)
        max_cell_x, max_cell_y = self._get_cell(
            entity.x + entity.world_units_width,
            entity.y + entity.world_units_height
        )
        
        cells = set()
        for cx in range(min_cell_x, max_cell_x + 1):
            for cy in range(min_cell_y, max_cell_y + 1):
                cells.add((cx, cy))
        return cells

    def insert(self, entity: 'Entity') -> None:
        """Insert an entity into the spatial hash."""
        cells = self._get_cells_for_entity(entity)
        for cell in cells:
            self._grid[cell].add(entity)
        self._entity_cells[entity] = cells

    def remove(self, entity: 'Entity') -> None:
        """Remove an entity from the spatial hash."""
        if entity in self._entity_cells:
            for cell in self._entity_cells[entity]:
                self._grid[cell].discard(entity)
                # Clean up empty cells to save memory
                if not self._grid[cell]:
                    del self._grid[cell]
            del self._entity_cells[entity]

    def update(self, entity: 'Entity') -> None:
        """Update an entity's position in the spatial hash."""
        new_cells = self._get_cells_for_entity(entity)
        old_cells = self._entity_cells.get(entity, set())
        
        # Only update if cells changed
        if new_cells != old_cells:
            # Remove from old cells that are no longer occupied
            for cell in old_cells - new_cells:
                self._grid[cell].discard(entity)
                if not self._grid[cell]:
                    del self._grid[cell]
            
            # Add to new cells
            for cell in new_cells - old_cells:
                self._grid[cell].add(entity)
            
            self._entity_cells[entity] = new_cells

    def query_region(self, min_x: float, min_y: float, max_x: float, max_y: float) -> List['Entity']:
        """
        Query all entities that may intersect the given region.
        Returns entities in cells that overlap with the query region.
        """
        min_cell_x, min_cell_y = self._get_cell(min_x, min_y)
        max_cell_x, max_cell_y = self._get_cell(max_x, max_y)
        
        result: Set[Entity] = set()
        for cx in range(min_cell_x, max_cell_x + 1):
            for cy in range(min_cell_y, max_cell_y + 1):
                cell_key = (cx, cy)
                if cell_key in self._grid:
                    result.update(self._grid[cell_key])
        
        return list(result)

    def query_point(self, x: float, y: float) -> List['Entity']:
        """Query all entities that may contain the given point."""
        cell = self._get_cell(x, y)
        if cell in self._grid:
            return list(self._grid[cell])
        return []

    def get_all_entities(self) -> List['Entity']:
        """Return all entities in the spatial hash."""
        return list(self._entity_cells.keys())

    def __contains__(self, entity: 'Entity') -> bool:
        """Check if an entity is in the spatial hash."""
        return entity in self._entity_cells

    def clear(self) -> None:
        """Clear all entities from the spatial hash."""
        self._grid.clear()
        self._entity_cells.clear()
