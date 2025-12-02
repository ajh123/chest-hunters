from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from world import World

import pygame
from world import Entity


class Camera(Entity):
    def __init__(self, world: World, width: int, height: int, speed: float = 0.1):
        image_map = {
            "default": "assets/player004.png"
        }
        super().__init__(world, 0, 0, width, height, image_map=image_map)  # Initialize the parent Entity class
        self.speed = speed
        self.set_image_state("default")
        self.health = 100

    def handle_input(self):
        """Read input and store movement vector."""
        keys = pygame.key.get_pressed()
        dx = dy = 0.0
        if keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_RIGHT]:
            dx += 1
        if keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_DOWN]:
            dy += 1
        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            factor = 0.7071  # 1/sqrt(2)
            dx *= factor
            dy *= factor
        self.set_velocity(dx * self.speed, dy * self.speed)

    def world_to_screen(self, world_x: int, world_y: int, tile_size: int) -> tuple[int, int]:
        # `self.x`/`self.y` are stored in world (tile) coordinates. Convert
        # them to pixel coordinates before subtracting from world positions.
        cam_px = int(self.x * tile_size)
        cam_py = int(self.y * tile_size)

        screen_x = int((world_x * tile_size) - cam_px + (self.width // 2))
        screen_y = int((world_y * tile_size) - cam_py + (self.height // 2))
        return screen_x, screen_y