from typing import TYPE_CHECKING, Tuple

import pygame
from constants import TILE_SIZE

if TYPE_CHECKING:
    from main import Game
    from player import Player
    from world import World
    from .image_utils import ImageLoader


class Renderer:
    def __init__(
            self,
            game: 'Game',
            player: 'Player',
            world: 'World',
            image_loader: 'ImageLoader'
        ):
        self.game = game
        self.player = player
        self.world = world
        self.image_loader = image_loader

    def render(self):
        self.renderTileMap()
        self.renderEntities()        

    def renderTileMap(self):
        # Determine visible tile range
        # player.x / y are in tile coordinates; convert player center to
        # pixel coordinates before computing visible tile ranges.
        cam_px = (self.player.x * TILE_SIZE)
        cam_py = (self.player.y * TILE_SIZE)

        start_x = int((cam_px - (self.game.display_width // 2)) // TILE_SIZE)
        end_x = int((cam_px + (self.game.display_width // 2)) // TILE_SIZE + 1)
        start_y = int((cam_py - (self.game.display_height // 2)) // TILE_SIZE)
        end_y = int((cam_py + (self.game.display_height // 2)) // TILE_SIZE + 1)

        for x in range(start_x, end_x):
            for y in range(start_y, end_y):            
                tile = self.world.get_tile_at(x, y)
                if tile:
                    image = self.image_loader.load(tile.image)
                    screen_x, screen_y = world_to_screen(x, y, self.player, self.game)
                    self.game.screen.blit(image, (screen_x, screen_y))

    def renderEntities(self):       
        min_x, min_y, max_x, max_y = get_screen_bounds(self.player, self.game)

        # Query only entities in the visible region using spatial hash
        visible_entities = self.world.get_entities_in_region(min_x, min_y, max_x, max_y)
        
        for entity in visible_entities:
            screen_x, screen_y = world_to_screen(entity.x, entity.y, self.player, self.game)
            img = entity.get_current_image()
            if img:
                img = self.image_loader.load(img)
                # Align entity sprite so its base sits on the tile row.
                # Many entity sprites are taller than a single tile; draw them
                # shifted up by the difference between sprite height and tile size.
                offset_y = img.get_height() - TILE_SIZE
                if offset_y < 0:
                    offset_y = 0
                self.game.screen.blit(img, (screen_x, screen_y - offset_y))

                if entity.health > 0 and entity.max_health > 0:
                    if entity.health < entity.max_health:
                        health_bar_width = 40
                        health_bar_height = 6
                        health_ratio = entity.health / entity.max_health
                        health_bar_x = screen_x + (img.get_width() - health_bar_width) // 2
                        health_bar_y = screen_y - offset_y - 10
                        
                        # Draw background bar (red)
                        pygame.draw.rect(
                            self.game.screen,
                            (255, 0, 0),
                            (health_bar_x, health_bar_y, health_bar_width, health_bar_height)
                        )
                        
                        # Draw foreground bar (green)
                        pygame.draw.rect(
                            self.game.screen,
                            (0, 255, 0),
                            (health_bar_x, health_bar_y, int(health_bar_width * health_ratio), health_bar_height)
                        )


def world_to_screen(world_x: float, world_y: float, player: 'Player', game: 'Game') -> Tuple[int, int]:
    """Convert world coordinates to screen coordinates based on the player position."""
    cam_px = int(player.x * TILE_SIZE)
    cam_py = int(player.y * TILE_SIZE)

    screen_x = int((world_x * TILE_SIZE) - cam_px + (game.display_width // 2))
    screen_y = int((world_y * TILE_SIZE) - cam_py + (game.display_height // 2))
    return screen_x, screen_y

def screen_to_world(screen_x: int, screen_y: int, player: 'Player', game: 'Game') -> Tuple[float, float]:
    """Convert screen coordinates to world coordinates based on the player position."""
    cam_px = int(player.x * TILE_SIZE)
    cam_py = int(player.y * TILE_SIZE)

    world_x = (screen_x + cam_px - (game.display_width // 2)) / TILE_SIZE
    world_y = (screen_y + cam_py - (game.display_height // 2)) / TILE_SIZE
    return world_x, world_y

def get_screen_bounds(player: 'Player', game: 'Game') -> Tuple[int, int, int, int]:
    """Get the world coordinate bounds of the player's visible area."""
    cam_px = int(player.x * TILE_SIZE)
    cam_py = int(player.y * TILE_SIZE)

    margin = 2  # Extra tiles of margin for large sprites
    min_x = (cam_px - (game.display_width // 2)) // TILE_SIZE - margin
    max_x = (cam_px + (game.display_width // 2)) // TILE_SIZE + margin
    min_y = (cam_py - (game.display_height // 2)) // TILE_SIZE - margin
    max_y = (cam_py + (game.display_height // 2)) // TILE_SIZE + margin
    return min_x, min_y, max_x, max_y
