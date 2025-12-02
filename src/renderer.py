import pygame
from camera import Camera
from tiles import TileMap

TILE_SIZE = 32

class Renderer:
    def __init__(self, screen: pygame.Surface, camera: Camera, tile_map: TileMap):
        self.screen = screen
        self.camera = camera
        self.tile_map = tile_map

    def render(self):
        self.screen.fill((0, 0, 0))

        self.renderTileMap()

        pygame.display.flip()

    def renderTileMap(self):
        # Determine visible tile range
        start_x = int((self.camera.x - self.camera.width // 2) // TILE_SIZE)
        end_x = int((self.camera.x + self.camera.width // 2) // TILE_SIZE + 1)
        start_y = int((self.camera.y - self.camera.height // 2) // TILE_SIZE)
        end_y = int((self.camera.y + self.camera.height // 2) // TILE_SIZE + 1)

        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                for layer in range(3):  # Assuming 3 layers for now
                    tile = self.tile_map.get_tile(x, y, layer)
                    if tile:
                        screen_x, screen_y = self.camera.world_to_screen(x, y, TILE_SIZE)
                        self.screen.blit(tile.image, (screen_x, screen_y))