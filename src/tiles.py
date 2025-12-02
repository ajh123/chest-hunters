import pygame
from loaders import load_image


class Tile:
    def __init__(self, name: str, image: pygame.Surface):
        self.name = name
        self.image = image

class TileMap:
    def __init__(self):
        self.tiles: dict[tuple[int, int, int], Tile] = {}

    def add_tile(self, x: int, y: int, tile: Tile, layer: int = 0):
        self.tiles[(x, y, layer)] = tile

    def get_tile(self, x: int, y: int, layer: int = 0) -> Tile | None:
        return self.tiles.get((x, y, layer))

    def remove_tile(self, x: int, y: int, layer: int = 0):
        self.tiles.pop((x, y, layer), None)

GRASS = Tile("grass", load_image("assets/0_0.png"))
DIRT = Tile("dirt", load_image("assets/32_64.png"))
TREE = Tile("tree", load_image("assets/tree.png"))