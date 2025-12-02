import pygame
from entity import Entity


class Camera(Entity):
    def __init__(self, width: int, height: int, speed: float = 5.0):
        super().__init__(0, 0, width, height, image_map={})  # Initialize the parent Entity class
        self.speed = speed

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
        screen_x = int((world_x * tile_size) - self.x + (self.width // 2))
        screen_y = int((world_y * tile_size) - self.y + (self.height // 2))
        return screen_x, screen_y