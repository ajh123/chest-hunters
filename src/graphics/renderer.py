import pygame
from camera import Camera, world_to_screen, get_screen_bounds
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
        min_x, min_y, max_x, max_y = get_screen_bounds(self.camera)
        
        # Query only entities in the visible region using spatial hash
        visible_entities = self.world.get_entities_in_region(min_x, min_y, max_x, max_y)
        
        for entity in visible_entities:
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

                if entity.health > 0 and entity.max_health > 0:
                    if entity.health < entity.max_health:
                        health_bar_width = 40
                        health_bar_height = 6
                        health_ratio = entity.health / entity.max_health
                        health_bar_x = screen_x + (img.get_width() - health_bar_width) // 2
                        health_bar_y = screen_y - offset_y - 10
                        
                        # Draw background bar (red)
                        pygame.draw.rect(
                            self.screen,
                            (255, 0, 0),
                            (health_bar_x, health_bar_y, health_bar_width, health_bar_height)
                        )
                        
                        # Draw foreground bar (green)
                        pygame.draw.rect(
                            self.screen,
                            (0, 255, 0),
                            (health_bar_x, health_bar_y, int(health_bar_width * health_ratio), health_bar_height)
                        )