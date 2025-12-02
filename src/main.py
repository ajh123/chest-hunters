import pygame
import random

from camera import Camera
from graphics import Renderer, ImageLoader, MessageLog
from entities import Chest, Tree, Zombie
from world import Tile, World

# Global tiles
GRASS = Tile("grass", "assets/0_0.png")
DIRT = Tile("dirt", "assets/32_64.png")


class Game:
    def __init__(self, width: int = 800, height: int = 600):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 20)
        self.running = True
        self.log = MessageLog(self.font)

        self.world = World(self.log)
        self.camera = Camera(self.screen.get_width(), self.screen.get_height())
        self.camera.set_world(self.world)

        self.loader = ImageLoader()
        self.renderer = Renderer(self.screen, self.camera, self.world, self.loader)

        random.seed(0)
        self.generate_tiles()

        self.fixed_dt = 1 / 60
        self.accumulator = 0
        self.last_time = pygame.time.get_ticks() / 1000

    def run(self):
        self.log.add("Welcome to Chest Hunters!", duration=15)
        self.log.add("Collect treasure from chests to upgrade your skills.", duration=15)
        self.log.add("Attack zombies to gain experience.", duration=15)
        while self.running:
            self.handle_events()
            self.update_timing()
            self.perform_fixed_updates()
            self.render()
            self.clock.tick(120)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode(
                    (event.w, event.h), pygame.RESIZABLE
                )
                self.camera.display_width = event.w
                self.camera.display_height = event.h
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.camera.handle_click(event.pos[0], event.pos[1])

        self.camera.handle_input()

    def update_timing(self):
        now = pygame.time.get_ticks() / 1000
        dt = now - self.last_time
        self.last_time = now
        self.accumulator += min(dt, 0.25)

    def perform_fixed_updates(self):
        while self.accumulator >= self.fixed_dt:
            self.update_world(self.fixed_dt)
            self.accumulator -= self.fixed_dt

    def update_world(self, dt: float):
        for entity in self.world.get_entities():
            entity.tick(dt)
        if random.random() < 0.007:
            self.spawn_zombies(5)

    def generate_tiles(self):
        tile_map = self.world.get_tile_map()
        excluded = [Camera]
        for x in range(-50, 50):
            for y in range(-50, 50):
                r = random.random()
                if (x + y) % 3 == 0:
                    tile_map.add_tile(x, y, DIRT)
                else:
                    tile_map.add_tile(x, y, GRASS)
                    if r < 0.1:
                        tree = Tree(x, y)
                        if not self.world.has_collision(tree, excluded):
                            tree.set_world(self.world)
                        else:
                            del tree
                
                if r < 0.005:
                    chest = Chest(x, y)
                    if not self.world.has_collision(chest, excluded):
                        chest.set_world(self.world)
                    else:
                        del chest

    def spawn_zombies(self, count: int):
        excluded = [Camera]
        for _ in range(count):
            x = random.randint(-50, 50)
            y = random.randint(-50, 50)
            zombie = Zombie(x, y)
            if not self.world.has_collision(zombie, excluded):
                zombie.set_world(self.world)
            else:
                del zombie

    def render(self):
        self.screen.fill((0, 0, 0))
        self.renderer.render()
        self.log.draw(self.screen)
        pygame.display.flip()


if __name__ == "__main__":
    Game().run()
