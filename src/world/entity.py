from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from player import Player

from .world import World
from constants import TILE_SIZE

class Entity:
    def __init__(self,
                 x: float,
                 y: float,
                 width: int,
                 height: int,
                 image_map: dict[str, str]
        ):
        self.world: World | None = None
        self.world_units_width = width / TILE_SIZE
        self.world_units_height = height / TILE_SIZE
        self.x = x
        self.y = y
        self.velocity_dx = 0.0
        self.velocity_dy = 0.0
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

        if self.velocity_dx == 0.0 and self.velocity_dy == 0.0:
            return

        target_x = self.x + (self.velocity_dx * dt)
        target_y = self.y + (self.velocity_dy * dt)
        orig_x, orig_y = self.x, self.y

        # Helper: test whether moving the entity to (cx, cy) would collide with another entity.
        # We temporarily set self.x/self.y so the world's AABB check uses the candidate position,
        # then restore the original coordinates immediately.
        def _collides_at(cx: float, cy: float) -> bool:
            if not self.world:
                return False

            saved_x, saved_y = self.x, self.y
            try:
                self.x, self.y = cx, cy
                return bool(self.world.has_collision(self))
            finally:
                self.x, self.y = saved_x, saved_y

        # 1) Combined move
        if not _collides_at(target_x, target_y):
            self.x, self.y = target_x, target_y
            self.world.update_entity_position(self)
            return

        # 2) Horizontal-only (from original Y)
        if not _collides_at(target_x, orig_y):
            # horizontal allowed
            self.x = target_x
        else:
            # blocked on X
            self.x = orig_x
            self.velocity_dx = 0.0

        # 3) Vertical (from whatever x we ended up with after horizontal attempt)
        if not _collides_at(self.x, target_y):
            self.y = target_y
        else:
            # blocked on Y
            self.y = orig_y
            self.velocity_dy = 0.0

        # Update spatial hash if position changed
        if self.x != orig_x or self.y != orig_y:
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
        self.velocity_dx = dx
        self.velocity_dy = dy

    def get_position(self) -> tuple[float, float]:
        return self.x, self.y
    
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
