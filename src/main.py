import pygame
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.init()

from camera import Camera
from tiles import TileMap, GRASS, DIRT, TREE
from renderer import Renderer

def generate_tiles(tile_map: TileMap):
    for x in range(-50, 50):
        for y in range(-50, 50):
            if (x + y) % 3 == 0:
                tile_map.add_tile(x, y, DIRT)
            else:
                tile_map.add_tile(x, y, GRASS)

                if (x + y) % 2 == 0:
                    tile_map.add_tile(x, y, TREE, layer=1)

def main():
    global screen
    clock = pygame.time.Clock()

    camera = Camera(screen.get_width(), screen.get_height())
    tile_map = TileMap()
    renderer = Renderer(screen, camera, tile_map)

    generate_tiles(tile_map)

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
        camera.tick()
        renderer.render()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()