from camera import Camera
from world import Entity
import time


class Chest(Entity):
    def __init__(self, x: float, y: float):
        images = {
            "closed": "assets/chest_closed.png",
            "open": "assets/chest_open.png"
        }
        super().__init__(x, y, 32, 32, images)
        self.set_image_state("closed")
        self.is_open = False
        self.delay = 0.0 # Delay in seconds before it can be opened again

    def interact(self, player: 'Camera'):
        if self.world is None:
            return

        distance = self.world.distance_between(self.x, self.y, player.x, player.y)
        if distance < 4:
            if not self.is_open and self.delay <= 0:
                self.is_open = True
                self.set_image_state("open")
                self.delay = time.time() + 1.0  # 1 second delay before it can be opened again
                self.world.log.add("The chest is a lie! It is completely empty.", duration=5)
        else:
            self.world.log.add("Too far to interact with the chest.")

    def tick(self, dt: float):
        super().tick(dt)
        if self.is_open and time.time() >= self.delay:
            self.is_open = False
            self.set_image_state("closed")
            self.delay = 0.0
        

class Tree(Entity):
    def __init__(self, x: float, y: float):
        images = {
            "default": "assets/jungle-tree_0.png"
        }
        super().__init__(x, y, 64, 64, images)
        self.set_image_state("default")


class Zombie(Entity):
    def __init__(self, x: float, y: float):
        images = {
            "default": "assets/zombie000.png"
        }
        super().__init__(x, y, 32, 64, images)
        self.set_image_state("default")
        self.health = 100
        self.max_health = 100

    def tick(self, dt: float):
        super().tick(dt)

        if not self.world:
            return

        # Simple random movement logic
        import random
        if random.random() < 0.1:
            self.set_velocity(random.uniform(-3, 3), random.uniform(-3, 3))

        # Simple attack logic here

        if random.random() < 0.05:
            res = self.world.entities_in_radius(self.x, self.y, 2, excluded=[Zombie])
            for entity in res:
                if isinstance(entity, Camera):
                    entity.take_damage(5)