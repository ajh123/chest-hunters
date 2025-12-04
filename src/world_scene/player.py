from typing import TYPE_CHECKING

import pygame
from .world_core import Entity
from .graphics import screen_to_world

if TYPE_CHECKING:
    from main import Game


class Player(Entity):
    def __init__(self, game: 'Game'):
        image_map = {
            "default": "textures/entities/player0.png"
        }
        super().__init__(0, 0, 30, 48, image_map=image_map)  # Initialize the parent Entity class

        self.game = game
        self.speed = 3
        self.attack_range = 3
        self.attack_damage = 15
        self.health = 100
        self.max_health = 100
        self.points = 0
        self.lives = 3

        self.set_image_state("default")

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
        from .entities import Zombie
        if not self.world:
            return

        world_x, world_y = screen_to_world(mouse_x, mouse_y, self, self.game)

        # Try to interact with an entity at the clicked position
        entity = self.world.point_collision(world_x, world_y, excluded=[Player])
        if entity:
            entity.interact(self)
    
        # Try attacking zombies in range
        result = self.world.entities_in_radius(self.x, self.y, self.attack_range, excluded=[Player])
        for zombie in result:
            if isinstance(zombie, Zombie):
                zombie.take_damage(self.attack_damage, self)

    def die(self):
        if not self.world:
            return

        self.world.is_frozen = True
        self.set_velocity(0, 0)
        self.lives -= 1
        self.x = 0
        self.y = 0
        self.world.update_entity_position(self)
        if self.lives <= 0:
            return

        self.health = 100
        self.max_health = 100
        self.world.is_frozen = False
