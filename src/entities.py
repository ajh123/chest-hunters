from player import Player
from world import Entity
import time
import random


class Chest(Entity):
    def __init__(self, x: float, y: float):
        images = {
            "closed": "textures/entities/chest_closed0.png",
            "open": "textures/entities/chest_open0.png"
        }
        super().__init__(x, y, 32, 32, images)
        self.set_image_state("closed")
        self.is_open = False
        self.delay = 0.0 # Delay in seconds before it can be opened again

    def interact(self, player: 'Player'):
        if self.world is None:
            return

        distance = self.world.distance_between(self.x, self.y, player.x, player.y)
        if distance < 4:
            if not self.is_open and self.delay <= 0:
                self.is_open = True
                self.set_image_state("open")
                self.delay = time.time() + 8.0  # 8 second delay before it can be opened again

                # Give player random points between 5 and 20
                points = random.randint(5, 20)
                player.points += points
                self.world.log.add(f"You found {points} points in the chest!")
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
            "default": "textures/entities/jungle_tree0.png"
        }
        super().__init__(x, y, 64, 64, images)
        self.set_image_state("default")


class Zombie(Entity):
    def __init__(self, x: float, y: float):
        images = {
            "default": "textures/entities/zombie0.png"
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
                if isinstance(entity, Player):
                    entity.take_damage(5)

    def take_damage(self, amount: float, attacker: 'Entity | None' = None):
        super().take_damage(amount, attacker=attacker)
        if isinstance(attacker, Player):
            if self.health > 0:
                points = random.randint(10, 20)
                attacker.points += points
                if self.world:
                    self.world.log.add(f"The zombie was damaged! +{points} points")
            else:
                points = random.randint(20, 40)
                attacker.points += points
                if self.world:
                    self.world.log.add(f"The zombie was defeated! +{points} points")
