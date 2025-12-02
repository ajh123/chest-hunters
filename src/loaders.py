import pygame

def load_image(path: str) -> pygame.Surface:
    res = pygame.Surface((32, 32))
    res.fill((255, 0, 255))  # Magenta placeholder

    try:
        res = pygame.image.load(path).convert_alpha()
    except FileNotFoundError as e:
        print(f"Error loading image: {e}")
    return res