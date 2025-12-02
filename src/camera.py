import pygame
from typing import Tuple
from constants import TILE_SIZE
from world import Entity


class Camera(Entity):
    def __init__(self, display_width: int, display_height: int):
        image_map = {
            "default": "assets/player004.png"
        }
        super().__init__(0, 0, 30, 48, image_map=image_map)  # Initialize the parent Entity class
        self.speed = 3
        self.attack_range = 3
        self.attack_damage = 15
        self.set_image_state("default")
        self.health = 100
        self.display_width = display_width
        self.display_height = display_height

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

    def handle_click(self, mouse_x: int, mouse_y: int):
        from entities import Zombie
        if not self.world:
            return

        world_x, world_y = screen_to_world(mouse_x, mouse_y, self)

        # Try to interact with an entity at the clicked position
        entity = self.world.point_collision(world_x, world_y, excluded=[Camera])
        if entity:
            entity.interact(self)
    
        # Try attacking zombies in range
        result = self.world.entities_in_radius(self.x, self.y, self.attack_range, excluded=[Camera])
        for zombie in result:
            if isinstance(zombie, Zombie):
                zombie.take_damage(self.attack_damage)

    def die(self):
        self.x = 0
        self.y = 0
        self.health = 100

def world_to_screen(world_x: float, world_y: float, camera: Camera) -> Tuple[int, int]:
    cam_px = int(camera.x * TILE_SIZE)
    cam_py = int(camera.y * TILE_SIZE)

    screen_x = int((world_x * TILE_SIZE) - cam_px + (camera.display_width // 2))
    screen_y = int((world_y * TILE_SIZE) - cam_py + (camera.display_height // 2))
    return screen_x, screen_y

def screen_to_world(screen_x: int, screen_y: int, camera: Camera) -> Tuple[float, float]:
    cam_px = int(camera.x * TILE_SIZE)
    cam_py = int(camera.y * TILE_SIZE)

    world_x = (screen_x + cam_px - (camera.display_width // 2)) / TILE_SIZE
    world_y = (screen_y + cam_py - (camera.display_height // 2)) / TILE_SIZE
    return world_x, world_y