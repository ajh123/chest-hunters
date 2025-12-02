import pygame


class ImageLoader:
    def __init__(self):
        self.cache: dict[str, pygame.Surface] = {}
    
    def load(self, path: str) -> pygame.Surface:
        if path not in self.cache:
            try:
                image = pygame.image.load(path).convert_alpha()
                self.cache[path] = image
            except FileNotFoundError as e:
                print(f"Error loading image: {e}")
                # Return a placeholder surface in case of error
                placeholder = pygame.Surface((32, 32))
                placeholder.fill((255, 0, 255))  # Magenta placeholder
                self.cache[path] = placeholder
        return self.cache[path]
