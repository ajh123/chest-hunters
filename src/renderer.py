import pygame
from camera import Camera
from world import World
from constants import TILE_SIZE


class Renderer:
    def __init__(
            self,
            screen: pygame.Surface,
            camera: Camera,
            world: World
        ):
        self.screen = screen
        self.camera = camera
        self.world = world

    def render(self):
        self.screen.fill((0, 0, 0))

        self.renderTileMap()
        self.renderEntities()

        pygame.display.flip()

    def renderTileMap(self):
        # Determine visible tile range
        start_x = int((self.camera.x - self.camera.width // 2) // TILE_SIZE)
        end_x = int((self.camera.x + self.camera.width // 2) // TILE_SIZE + 1)
        start_y = int((self.camera.y - self.camera.height // 2) // TILE_SIZE)
        end_y = int((self.camera.y + self.camera.height // 2) // TILE_SIZE + 1)

        for x in range(start_x, end_x):
            for y in range(start_y, end_y):            
                tile = self.world.get_tile_at(x, y)
                if tile:
                    screen_x, screen_y = self.camera.world_to_screen(x, y, TILE_SIZE)
                    #print(f"Rendering tile at world ({x}, {y}) to screen ({screen_x}, {screen_y})")
                    self.screen.blit(tile.image, (screen_x, screen_y))

    def renderEntities(self):
        for entity in self.world.get_entities():
            screen_x, screen_y = self.camera.world_to_screen(entity.x, entity.y, TILE_SIZE)
            #print(f"Rendering entity at world ({entity.x}, {entity.y}) to screen ({screen_x}, {screen_y})")
            img = entity.get_current_image()
            if img:
                # Align entity sprite so its base sits on the tile row.
                # Many entity sprites are taller than a single tile; draw them
                # shifted up by the difference between sprite height and tile size.
                offset_y = img.get_height() - TILE_SIZE
                if offset_y < 0:
                    offset_y = 0
                self.screen.blit(img, (screen_x, screen_y - offset_y))