from __future__ import annotations
import pygame
from typing import TYPE_CHECKING, List

from .scene import Scene

if TYPE_CHECKING:
    from main import Game


class MenuScene(Scene):
    TITLE = "Chest Hunters"

    def __init__(self, game: Game):
        super().__init__(game)
        self.title_font = pygame.font.SysFont("arial", 48)
        self.subtitle_font = pygame.font.SysFont("arial", 24)

    def handle_events(self, events: List[pygame.event.Event]):
        for ev in events:
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    from scenes.world_scene import WorldScene
                    self.game.set_scene(WorldScene(self.game))

            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    from scenes.world_scene import WorldScene
                    self.game.set_scene(WorldScene(self.game))

    def fixed_update(self, dt: float):
        # Menu has no deterministic simulation
        pass

    def update(self, dt: float):
        # Frame-dependent animations could go here
        pass

    def render(self, screen: pygame.Surface, alpha: float):
        screen.fill((0, 0, 0))
        w, h = screen.get_size()

        title = self.title_font.render(self.TITLE, True, (255, 255, 255))
        title_rect = title.get_rect(center=(w // 2, h // 2 - 50))
        screen.blit(title, title_rect)

        subtitle = "Press Enter or Click to start"
        subtitle_surf = self.subtitle_font.render(subtitle, True, (200, 200, 200))
        subtitle_rect = subtitle_surf.get_rect(center=(w // 2, h // 2 + 20))
        screen.blit(subtitle_surf, subtitle_rect)

        pygame.display.flip()
