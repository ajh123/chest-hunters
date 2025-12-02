from world import World, Entity


class Chest(Entity):
    def __init__(self, world: World, x: float, y: float):
        images = {
            "closed": "assets/chest_closed.png",
            "open": "assets/chest_open.png"
        }
        super().__init__(world, x, y, 32, 32, images)
        self.set_image_state("closed")
        self.is_open = False

    def toggle(self):
        if self.is_open:
            self.set_image_state("closed")
        else:
            self.set_image_state("open")
        self.is_open = not self.is_open


class Tree(Entity):
    def __init__(self, world: World, x: float, y: float):
        images = {
            "default": "assets/jungle-tree_0.png"
        }
        super().__init__(world, x, y, 64, 64, images)
        self.set_image_state("default")


class Zombie(Entity):
    def __init__(self, world: World, x: float, y: float):
        images = {
            "default": "assets/zombie000.png"
        }
        super().__init__(world, x, y, 32, 64, images)
        self.set_image_state("default")
        self.health = 100

    def tick(self):
        super().tick()
        # Simple random movement logic
        import random
        if random.random() < 0.1:
            self.set_velocity(random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1))