from .world import World
from .utils import is_entity_at

class Entity:
    def __init__(self,
                 world: World,
                 x: float,
                 y: float,
                 width: int,
                 height: int,
                 image_map: dict[str, str]
        ):
        self.world = world
        self.world.add_entity(self)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.velocity_dx = 0.0
        self.velocity_dy = 0.0
        self.image_map = image_map
        self.current_image_key: str | None = None
        self.health = -1 # -1 means infinite health

    def tick(self):
        """Update entity position based on its velocity with basic collision checking.

        This performs a simple entity-vs-entity AABB-style check using
        `is_entity_at`. It first attempts the combined move; if blocked,
        it tries axis-separated moves so entities can slide along obstacles.
        When a collision is detected on an axis, the corresponding
        velocity component is zeroed to prevent repeated collision.
        """

        # No movement -> nothing to do
        if self.velocity_dx == 0.0 and self.velocity_dy == 0.0:
            return

        target_x = self.x + self.velocity_dx
        target_y = self.y + self.velocity_dy

        # exclude self from collision checks
        excluded = [self]

        # If combined movement is free, apply both
        if is_entity_at(self.world, int(target_x), int(target_y), excluded) is None:
            self.x = target_x
            self.y = target_y
            return

        # Try horizontal move only
        if is_entity_at(self.world, int(target_x), int(self.y), excluded) is None:
            self.x = target_x
        else:
            # Blocked on X axis
            self.velocity_dx = 0.0

        # Try vertical move only
        if is_entity_at(self.world, int(self.x), int(target_y), excluded) is None:
            self.y = target_y
        else:
            # Blocked on Y axis
            self.velocity_dy = 0.0

    def take_damage(self, amount: float):
        if self.health < 0:
            return  # Infinite health

        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        self.world.get_entities().remove(self)

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
