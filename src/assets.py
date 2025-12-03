import pygame
import os
from io import BytesIO


class AssetManager:
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.cache: dict[str, bytes] = {}
    
    def load_assets(self):
        # Recursively load all assets from the base path We also need to support subdirectories
        # Assets can be any file type; here we just store their paths and contents

        def _load_directory(self: AssetManager, current_path: str):
            for entry in os.scandir(current_path):
                if entry.is_dir():
                    _load_directory(self, entry.path)
                else:
                    relative_path = os.path.relpath(entry.path, self.base_path)
                    try:
                        with open(entry.path, 'rb') as f:
                            # Normalize to use forward slashes in keys
                            relative_path = relative_path.replace('\\', '/')
                            self.cache[relative_path] = f.read()
                    except Exception as e:
                        print(f"Error loading asset {relative_path}: {e}")

        _load_directory(self, self.base_path)

    def get_asset(self, relative_path: str) -> bytes | None:
        return self.cache.get(relative_path)
    
    def get_absolute_path(self, relative_path: str) -> str | None:
        absolute_path = os.path.join(self.base_path, relative_path)
        if os.path.exists(absolute_path):
            return absolute_path
        return None
    
    def try_get_image(self, relative_path: str) -> pygame.Surface:
        asset_data = self.get_asset(relative_path)
        if asset_data is not None:
            try:
                image_file = BytesIO(asset_data)
                image = pygame.image.load(image_file).convert_alpha()
                return image
            except Exception as e:
                print(f"Error converting asset to image {relative_path}: {e}")
        # Return fallback magenta surface if loading fails
        fallback = pygame.Surface((32, 32))
        fallback.fill((255, 0, 255))
        return fallback
