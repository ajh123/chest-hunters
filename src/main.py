import pygame
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.init()

from camera import Camera
from renderer import Renderer
from entities import Chest, Tree, Zombie
from world import Tile, World, is_entity_at
from file_utils import ImageLoader

import random

GRASS = Tile("grass", "assets/0_0.png")
DIRT = Tile("dirt", "assets/32_64.png")

def generate_tiles(world: World):
    random.seed(0)
    r = random.random()
    tile_map = world.get_tile_map()
    excluded = [Camera]
    for x in range(-50, 50):
        for y in range(-50, 50):
            r = random.random()
            if (x + y) % 3 == 0:
                tile_map.add_tile(x, y, DIRT)
            else:
                tile_map.add_tile(x, y, GRASS)
                if r < 0.1:
                    if not is_entity_at(world, x, y, excluded):
                        Tree(world, x, y)
            if r < 0.005:
                if not is_entity_at(world, x, y, excluded):
                    Chest(world, x, y)

def random_zombies(world: World, count: int):
    excluded = [Camera]
    for _ in range(count):
        x = random.randint(-50, 50)
        y = random.randint(-50, 50)
        
        if not is_entity_at(world, x, y, excluded):
            Zombie(world, x, y)

def main():
    global screen
    random.seed(0)
    clock = pygame.time.Clock()
    world = World()
    camera = Camera(world, screen.get_width(), screen.get_height())
    image_loader = ImageLoader()
    renderer = Renderer(screen, camera, world, image_loader)

    generate_tiles(world)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                camera.width = event.w
                camera.height = event.h

        camera.handle_input()

        for entity in world.get_entities():
            entity.tick()

        r = random.random()
        if r < 0.007:
            random_zombies(world, 5)

        renderer.render()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()