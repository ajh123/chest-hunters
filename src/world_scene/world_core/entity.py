from typing import TYPE_CHECKING, Tuple, Dict
if TYPE_CHECKING:
    from ..player import Player

from .world import World
from ..constants import TILE_SIZE

class Entity:
    def __init__(self,
                 x: float,
                 y: float,
                 width: int,
                 height: int,
                 image_map: Dict[str, str]
        ):
        self.world: World | None = None
        self.size_world_units = (width / TILE_SIZE, height / TILE_SIZE)
        self.pos = (x, y)
        self.velocity = (0.0, 0.0)
        self.image_map = image_map
        self.current_image_key: str | None = None
        self.health = -1 # -1 means infinite health
        self.max_health = -1

    def set_world(self, world: World):
        self.world = world
        world.add_entity(self)

    def tick(self, dt: float):
        """Move applying simple AABB entity-vs-entity collision using World.has_collision.

        Strategy:
        1) Compute target (x, y).
        2) Test combined move at (target_x, target_y). If free, apply both and return.
        3) Test horizontal-only at (target_x, orig_y). If free, apply x (keep trying vertical later).
        Otherwise treat X as blocked and zero velocity_dx.
        4) Test vertical at (current_x, target_y). If free, apply y. Otherwise treat Y as blocked
        and zero velocity_dy.

        This uses temporary position changes only for collision testing; it relies on
        World.has_collision ignoring the source entity (your implementation does).
        """
        if not self.world:
            return

        if self.velocity == (0.0, 0.0):
            return

        target_x = self.pos[0] + (self.velocity[0] * dt)
        target_y = self.pos[1] + (self.velocity[1] * dt)
        orig_x, orig_y = self.pos

        # Helper: test whether moving the entity to (cx, cy) would collide with another entity.
        # We temporarily set self.x/self.y so the world's AABB check uses the candidate position,
        # then restore the original coordinates immediately.
        def _collides_at(target: Tuple[float, float]) -> bool:
            if not self.world:
                return False

            saved_pos = self.pos
            try:
                self.pos = target
                return bool(self.world.has_collision(self))
            finally:
                self.pos = saved_pos

        # 1) Combined move
        if not _collides_at((target_x, target_y)):
            self.pos = (target_x, target_y)
            self.world.update_entity_position(self)
            return

        # 2) Horizontal-only (from original Y)
        if not _collides_at((target_x, orig_y)):
            # horizontal allowed
            self.pos = (target_x, self.pos[1])
        else:
            # blocked on X
            self.pos = (orig_x, self.pos[1])
            self.velocity = (0.0, self.velocity[1])

        # 3) Vertical (from whatever x we ended up with after horizontal attempt)
        if not _collides_at((self.pos[0], target_y)):
            self.pos = (self.pos[0], target_y)
        else:
            # blocked on Y
            self.y = orig_y
            self.velocity_dy = 0.0

        # Update spatial hash if position changed
        if self.pos != (orig_x, orig_y):
            self.world.update_entity_position(self)

    def interact(self, player: 'Player'):
        pass

    def take_damage(self, amount: float, attacker: 'Entity | None' = None):
        if self.health < 0:
            return  # Infinite health

        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        if not self.world:
            return

        self.world.remove_entity(self)

    def set_velocity(self, dx: float, dy: float):
        self.velocity = (dx, dy)

    def get_position(self) -> Tuple[float, float]:
        return self.pos
    
    def set_image_state(self, key: str):
        if key in self.image_map:
            self.current_image_key = key

    def get_current_image(self) -> str | None:
        if self.current_image_key:
            return self.image_map[self.current_image_key]
        return None

    def __del__(self):
        # Remove from world on garbage collection
        if self.world:
            self.world.remove_entity(self)
