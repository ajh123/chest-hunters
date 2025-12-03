import pygame
import pygame_gui
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from player import Player


class HUD:
    """HUD showing health, points, and lives in the top-left corner using pygame_gui."""
    
    PANEL_WIDTH = 220
    PANEL_HEIGHT = 120
    PADDING = 8

    def __init__(
        self,
        manager: pygame_gui.UIManager,
        player: "Player | None" = None,
    ):
        self._player = player
        self.manager = manager

        # Create a panel in the top-left corner with semi-transparent background
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((self.PADDING, self.PADDING), (self.PANEL_WIDTH, self.PANEL_HEIGHT)),
            manager=self.manager,
            object_id="#info_panel",
        )

        bar_width = self.PANEL_WIDTH - self.PADDING * 2

        # Health bar
        self.health_bar = pygame_gui.elements.UIStatusBar(
            relative_rect=pygame.Rect((self.PADDING, self.PADDING), (bar_width, 25)),
            manager=self.manager,
            container=self.panel
        )

        # Health label (centered on top of health bar)
        self.health_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.PADDING, self.PADDING), (bar_width, 25)),
            text="Health",
            manager=self.manager,
            container=self.panel,
            parent_element=self.panel,
            object_id="#info_panel/centered_message"
        )

        # Points label (left-aligned with health bar)
        points_text = f"Points: {self._player.points}" if self._player else "Points: 0"
        self.points_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.PADDING, 40), (bar_width, 30)),
            text=points_text,
            manager=self.manager,
            container=self.panel,
            parent_element=self.panel,
            object_id="#info_panel/message"
        )

        # Lives label (left-aligned with health bar)
        lives_text = f"Lives: {self._player.lives}" if self._player else "Lives: 0"
        self.lives_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.PADDING, 75), (bar_width, 30)),
            text=lives_text,
            manager=self.manager,
            container=self.panel,
            parent_element=self.panel,
            object_id="#info_panel/message"
        )

    @property
    def player(self) -> "Player | None":
        return self._player

    @player.setter
    def player(self, value: "Player"):
        self._player = value

    def update(self):
        """Update HUD values from player state."""
        if self._player is None:
            return

        # Update health bar
        health_percent = self._player.health / self._player.max_health
        self.health_bar.percent_full = health_percent

        # Update labels
        self.points_label.set_text(f"Points: {self._player.points}")
        self.lives_label.set_text(f"Lives: {self._player.lives}")

    def handle_resize(self):
        """Handle window resize - HUD stays in top-left, no repositioning needed."""
        # The panel is anchored to top-left, so no repositioning needed
        pass
