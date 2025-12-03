import pygame
import pygame_gui
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    pass


class Message:
    """Represents a single message in the log with its UI label."""
    def __init__(
        self,
        manager: pygame_gui.UIManager,
        container: pygame_gui.elements.UIPanel,
        text: str,
        y_position: int,
        width: int
    ):
        self.text: str = text
        self.manager = manager
        self.container = container

        # Create a label for this message
        self.label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((5, y_position), (width - 10, 25)),
            text=text,
            manager=manager,
            container=container,
            object_id="#info_panel/message"
        )

    def kill(self):
        """Remove the UI element."""
        self.label.kill()


class MessageLog:
    """A reusable message log for PyGame using pygame_gui, anchored to bottom-left."""

    PANEL_WIDTH = 400
    PANEL_HEIGHT = 200
    PADDING = 8
    MESSAGE_HEIGHT = 35

    def __init__(self, manager: pygame_gui.UIManager, screen_height: int, max_messages: int = 10):
        self.manager = manager
        self.max_messages: int = max_messages
        self.messages: List[Message] = []
        self.screen_height = screen_height

        # Create a panel at the bottom-left
        panel_y = screen_height - self.PANEL_HEIGHT - self.PADDING
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((self.PADDING, panel_y), (self.PANEL_WIDTH, self.PANEL_HEIGHT)),
            manager=self.manager,
            object_id="#info_panel",
        )

    def add(self, text: str):
        # Remove oldest message if at capacity
        if len(self.messages) >= self.max_messages:
            old_message = self.messages.pop(0)
            old_message.kill()

        # Calculate y position for new message (at the bottom of existing messages)
        y_position = self.PANEL_HEIGHT - self.MESSAGE_HEIGHT - self.PADDING - (len(self.messages) * self.MESSAGE_HEIGHT)

        message = Message(
            manager=self.manager,
            container=self.panel,
            text=text,
            y_position=y_position,
            width=self.PANEL_WIDTH,
        )
        self.messages.append(message)
        self._reposition_messages()

    def _reposition_messages(self):
        """Reposition all message labels from bottom to top."""
        for i, message in enumerate(reversed(self.messages)):
            y_position = self.PANEL_HEIGHT - self.MESSAGE_HEIGHT - self.PADDING - (i * self.MESSAGE_HEIGHT)
            message.label.set_relative_position((5, y_position))

    def handle_resize(self, screen_height: int):
        """Handle window resize by repositioning the panel."""
        self.screen_height = screen_height
        panel_y = screen_height - self.PANEL_HEIGHT - self.PADDING
        self.panel.set_position((self.PADDING, panel_y))
