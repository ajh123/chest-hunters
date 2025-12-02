import pygame
import time
from typing import List, Tuple

class Message:
    """Represents a single message in the log."""
    def __init__(
        self, 
        font: pygame.font.Font,
        text: str, 
        duration: float = 3, 
        color: Tuple[int, int, int] = (255, 255, 255), 
        bg_color: Tuple[int, int, int] = (0, 0, 0), 
        padding: int = 5
    ):
        self.text: str = text
        self.duration: float = duration
        self.start_time: float = time.time()
        self.font: pygame.font.Font = font
        self.color: Tuple[int, int, int] = color
        self.bg_color: Tuple[int, int, int] = bg_color
        self.padding: int = padding

        self.surface: pygame.Surface = font.render(text, True, color)
        self.rect: pygame.Rect = self.surface.get_rect()

    def age(self) -> float:
        return time.time() - self.start_time

    def alpha(self) -> int:
        """Alpha for both text and background based on age."""
        elapsed = self.age()
        if elapsed >= self.duration:
            return 0
        return int(255 * (1 - elapsed / self.duration))

    def is_expired(self) -> bool:
        return self.age() >= self.duration


class MessageLog:
    """A reusable message log for PyGame with fading backgrounds."""
    def __init__(self, font: pygame.font.Font, max_messages: int = 10, padding: int = 5):
        self.font: pygame.font.Font = font
        self.max_messages: int = max_messages
        self.padding: int = padding
        self.messages: List[Message] = []

    def add(self, text: str, duration: float = 10, color: Tuple[int, int, int] = (255, 255, 255), bg_color: Tuple[int, int, int] = (0, 0, 0)):
        message = Message(
            font=self.font,
            text=text,
            duration=duration,
            color=color,
            bg_color=bg_color,
            padding=self.padding
        )
        self.messages.append(message)
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)

    def draw(self, surface: pygame.Surface):
        y_offset = surface.get_height() - self.padding
        self.messages = [m for m in self.messages if not m.is_expired()]

        for message in reversed(self.messages):
            alpha = message.alpha()
            if alpha <= 0:
                continue

            # Render text with alpha
            text_surf = message.font.render(message.text, True, message.color)
            text_surf.set_alpha(alpha)
            text_rect = text_surf.get_rect(bottomleft=(self.padding, y_offset))

            # Draw fading background
            bg_surf = pygame.Surface((text_rect.width + 2 * message.padding, text_rect.height + 2 * message.padding))
            bg_surf.set_alpha(alpha)
            bg_surf.fill(message.bg_color)
            surface.blit(bg_surf, (text_rect.left - message.padding, text_rect.top - message.padding))

            # Draw text on top
            surface.blit(text_surf, text_rect)
            y_offset -= text_rect.height + self.padding

