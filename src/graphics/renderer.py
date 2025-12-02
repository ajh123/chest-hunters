import pygame
from camera import Camera, world_to_screen
from world import World
from constants import TILE_SIZE
from .image_utils import ImageLoader


class Renderer:
    def __init__(
            self,
            screen: pygame.Surface,
            camera: Camera,
            world: World,
            image_loader: ImageLoader
        ):
        self.screen = screen
        self.camera = camera
        self.world = world
        self.image_loader = image_loader

    def render(self):
        self.renderTileMap()
        self.renderEntities()        

    def renderTileMap(self):
        # Determine visible tile range
        # Camera.x / y are in tile coordinates; convert camera center to
        # pixel coordinates before computing visible tile ranges.
        cam_px = (self.camera.x * TILE_SIZE)
        cam_py = (self.camera.y * TILE_SIZE)

        start_x = int((cam_px - (self.camera.display_width // 2)) // TILE_SIZE)
        end_x = int((cam_px + (self.camera.display_width // 2)) // TILE_SIZE + 1)
        start_y = int((cam_py - (self.camera.display_height // 2)) // TILE_SIZE)
        end_y = int((cam_py + (self.camera.display_height // 2)) // TILE_SIZE + 1)

        for x in range(start_x, end_x):
            for y in range(start_y, end_y):            
                tile = self.world.get_tile_at(x, y)
                if tile:
                    image = self.image_loader.load(tile.image)
                    screen_x, screen_y = world_to_screen(x, y, self.camera)
                    self.screen.blit(image, (screen_x, screen_y))

    def renderEntities(self):
        for entity in self.world.get_entities():
            screen_x, screen_y = world_to_screen(entity.x, entity.y, self.camera)
            img = entity.get_current_image()
            if img:
                img = self.image_loader.load(img)
                # Align entity sprite so its base sits on the tile row.
                # Many entity sprites are taller than a single tile; draw them
                # shifted up by the difference between sprite height and tile size.
                offset_y = img.get_height() - TILE_SIZE
                if offset_y < 0:
                    offset_y = 0
                self.screen.blit(img, (screen_x, screen_y - offset_y))

