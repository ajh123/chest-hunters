import pygame
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.init()

from camera import Camera
from tiles import GRASS, DIRT
from renderer import Renderer
from entities import Chest, Tree
from world import World

import random

def generate_tiles(world: World):
    random.seed(0)
    r = random.random()
    tile_map = world.get_tile_map()
    entities = world.get_entities()
    for x in range(-50, 50):
        for y in range(-50, 50):
            r = random.random()
            if (x + y) % 3 == 0:
                tile_map.add_tile(x, y, DIRT)
            else:
                tile_map.add_tile(x, y, GRASS)
                if r < 0.1:
                    print(world.is_entity_at(x, y))
                    if not world.is_entity_at(x, y):
                        tree = Tree(x, y)
                        entities.append(tree)
            if r < 0.005:
                if not world.is_entity_at(x, y):
                    chest = Chest(x, y)
                    entities.append(chest)

def main():
    global screen
    clock = pygame.time.Clock()
    world = World()

    camera = Camera(screen.get_width(), screen.get_height())
    world.add_entity(camera)

    renderer = Renderer(screen, camera, world)

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

        renderer.render()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()