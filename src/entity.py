import pygame

class Entity:
    def __init__(self, x: float, y: float, width: int, height: int, image_map: dict[str, pygame.Surface]):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.velocity_dx = 0.0
        self.velocity_dy = 0.0
        self.image_map = image_map
        self.current_image_key: str | None = None

    def tick(self):
        """Update entity position based on its velocity."""
        self.x += self.velocity_dx
        self.y += self.velocity_dy

    def set_velocity(self, dx: float, dy: float):
        self.velocity_dx = dx
        self.velocity_dy = dy

    def get_position(self) -> tuple[float, float]:
        return self.x, self.y
    
    def set_image_state(self, key: str):
        if key in self.image_map:
            self.current_image_key = key

    def get_current_image(self) -> pygame.Surface | None:
        if self.current_image_key:
            return self.image_map[self.current_image_key]
        return None
