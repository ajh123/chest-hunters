from loaders import load_image
from entity import Entity


class Chest(Entity):
    def __init__(self, x: float, y: float):
        images = {
            "closed": load_image("assets/chest_closed.png"),
            "open": load_image("assets/chest_open.png")
        }
        super().__init__(x, y, 32, 32, images)
        self.set_image_state("closed")
        self.is_open = False

    def toggle(self):
        if self.is_open:
            self.set_image_state("closed")
        else:
            self.set_image_state("open")
        self.is_open = not self.is_open


class Tree(Entity):
    def __init__(self, x: float, y: float):
        images = {
            "default": load_image("assets/jungle-tree_0.png")
        }
        super().__init__(x, y, 64, 64, images)
        self.set_image_state("default")