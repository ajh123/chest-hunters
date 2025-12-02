class Tile:
    def __init__(self, name: str, image: str):
        self.name = name
        self.image = image

class TileMap:
    def __init__(self):
        self.tiles: dict[tuple[int, int], Tile] = {}

    def add_tile(self, x: int, y: int, tile: Tile):
        self.tiles[(x, y)] = tile

    def get_tile(self, x: int, y: int) -> Tile | None:
        return self.tiles.get((x, y))

    def remove_tile(self, x: int, y: int):
        self.tiles.pop((x, y), None)


