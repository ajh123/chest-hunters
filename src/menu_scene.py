from typing import TYPE_CHECKING, List

import pygame
import pygame_gui

if TYPE_CHECKING:
    from main import Game

from scene import Scene


class MenuScene(Scene):
    TITLE = "Chest Hunters"


    def __init__(self, game: 'Game'):
        super().__init__(game)

        screen_w = self.game.display_width
        screen_h = self.game.display_height
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0, 0), (screen_w/2, screen_h)),
            manager=self.game.ui_manager,
        )

        # Title label inside the panel
        self.title_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 20), (screen_w/2, 50)),
            text=self.TITLE,
            manager=self.game.ui_manager,
            container=self.panel,
        )

        # Start button inside the panel, centered horizontally
        button_width = 200
        button_x = (screen_w/2 - button_width) // 2
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, 70), (button_width, 50)),
            text="Start Game",
            manager=self.game.ui_manager,
            container=self.panel,
        )

    def handle_events(self, events: List[pygame.event.Event]):
        # UI manager handles its own events
        for event in events:
            self.game.ui_manager.process_events(event)
            if event.type == pygame.VIDEORESIZE:
                # Recenter the panel on window resize
                self.panel.set_position((0, 0))
                self.panel.set_dimensions((self.game.display_width / 2, self.game.display_height))
                self.title_label.set_position((
                    (self.game.display_width / 2 - self.title_label.get_relative_rect().width) // 2,
                    self.title_label.get_relative_rect().y
                ))
                self.start_button.set_position((
                    (self.game.display_width / 2 - self.start_button.get_relative_rect().width) // 2,
                    self.start_button.get_relative_rect().y
                ))
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_button:
                    from world_scene import WorldScene, WorldSettings
                    settings = WorldSettings(seed=0, max_waves=10)
                    self.game.set_scene(lambda: WorldScene(self.game, settings))
