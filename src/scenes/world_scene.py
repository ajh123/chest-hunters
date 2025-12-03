from __future__ import annotations
import pygame
from typing import TYPE_CHECKING, List

from .scene import Scene
from graphics import Renderer, ImageLoader, MessageLog, HUD, get_screen_bounds
from world import Tile, World
from entities import Chest, Tree, Zombie, Player
import random

if TYPE_CHECKING:
    from main import Game
    from player import Player

# Global tiles
GRASS = Tile("grass", "assets/0_0.png")
DIRT = Tile("dirt", "assets/32_64.png")


class WorldScene(Scene):
    def __init__(self, game: Game):
        super().__init__(game)

        self.font = pygame.font.SysFont("arial", 20)
        self.log = MessageLog(self.font)

        self.world = World(self.log)
        self.player = Player(game)
        self.player.set_world(self.world)

        self.hud = HUD(self.font, self.player)
        self.loader = ImageLoader()
        self.renderer = Renderer(self.game, self.player, self.world, self.loader)

        random.seed(0)
        self._generate_tiles()

        # Optional welcome messages
        self.log.add("Welcome to Chest Hunters!", duration=15)
        self.log.add("Collect points from chests to upgrade your skills.", duration=15)
        self.log.add("Attack zombies to gain points.", duration=15)

    # ----------------------------------------------------------------------
    # Scene interface
    # ----------------------------------------------------------------------

    def handle_events(self, events: List[pygame.event.Event]):
        for ev in events:
            if not self.world.is_frozen and ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    self.player.handle_click(ev.pos[0], ev.pos[1])

        self.player.handle_input()

    def fixed_update(self, dt: float):
        if self.world.is_frozen:
            return
        min_x, min_y, max_x, max_y = get_screen_bounds(self.player, self.game)
        entities = self.world.get_entities_in_region(min_x, min_y, max_x, max_y)

        for ent in entities:
            ent.tick(dt)

        # Zombie spawning – deterministic, fixed-rate
        if random.random() < 0.007:
            self._spawn_zombies(5)

    def update(self, dt: float):
        # Frame-only effects (UI animations, smoothing)
        pass

    def render(self, screen: pygame.Surface, alpha: float):
        screen.fill((0, 0, 0))

        # If desired, you can supply alpha to renderer for interpolation
        self.renderer.render()
        self.log.draw(screen)
        self.hud.draw(screen)

        pygame.display.flip()

    # ----------------------------------------------------------------------
    # Internal helpers
    # ----------------------------------------------------------------------

    def _generate_tiles(self):
        tile_map = self.world.get_tile_map()

        for x in range(-50, 50):
            for y in range(-50, 50):
                r = random.random()

                if (x + y) % 3 == 0:
                    tile_map.add_tile(x, y, DIRT)
                else:
                    tile_map.add_tile(x, y, GRASS)
                    if r < 0.1:
                        tree = Tree(x, y)
                        if not self.world.has_collision(tree):
                            tree.set_world(self.world)
                        else:
                            del tree

                if r < 0.005:
                    chest = Chest(x, y)
                    if not self.world.has_collision(chest):
                        chest.set_world(self.world)
                    else:
                        del chest

    def _spawn_zombies(self, count: int):
        for _ in range(count):
            x = random.randint(-50, 50)
            y = random.randint(-50, 50)
            zombie = Zombie(x, y)
            if not self.world.has_collision(zombie):
                zombie.set_world(self.world)
            else:
                del zombie
