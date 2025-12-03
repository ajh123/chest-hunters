from __future__ import annotations
import pygame
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from main import Game


class Scene:
    """Base scene API.

    Scenes receive:
      - handle_events(events)
      - fixed_update(dt)    # called at a fixed timestep (game logic)
      - update(dt)          # called once per frame for non-critical updates/animations
      - render(screen, alpha)  # render, alpha is interpolation factor [0..1]
    """

    def __init__(self, game: 'Game'):
        self.game = game

    def handle_events(self, events: List[pygame.event.Event]):
        pass

    def fixed_update(self, dt: float):
        """Deterministic logic — called from the global fixed-step loop."""
        pass

    def update(self, dt: float):
        """Frame-dependent updates (input smoothing, UI animations)."""
        pass

    def render(self, screen: pygame.Surface, alpha: float):
        """Draw the scene. alpha is interpolation fraction for rendering between fixed steps."""
        pass

    def on_leave(self):
        """Called when the scene is being replaced."""
        self.game.ui_manager.clear_and_reset()