from typing import TYPE_CHECKING, List
from dataclasses import dataclass
import pygame

from .graphics import MessageLog, HUD, Renderer, get_screen_bounds
from .world_core import Tile, World
from .entities import Chest, Tree, Zombie, Player
import random
from scene import Scene
from .waves import Wave, WaveManager

if TYPE_CHECKING:
    from main import Game
    from .player import Player

# Global tiles
GRASS = Tile("grass", "textures/tiles/grass0.png")
DIRT = Tile("dirt", "textures/tiles/dirt0.png")


@dataclass
class WorldSettings:
    seed: int
    max_waves: int


class WorldScene(Scene):
    def __init__(self, game: 'Game', settings: WorldSettings):
        super().__init__(game)

        # Create UI elements with the UI manager first (World needs log)
        self.log = MessageLog(self.game.ui_manager, self.game.display_height)

        self.settings = settings
        self.world = World(self.log)
        self.player = Player(game)
        self.player.set_world(self.world)
        self.wave_manager = WaveManager(self._make_wave(1))

        self.hud = HUD(self.game.ui_manager, self.player, self.wave_manager, self.game)

        self.renderer = Renderer(self.game, self.player, self.world)

        random.seed(self.settings.seed)
        self._generate_tiles()
        self.wave_manager.start_next_wave()

        # Optional welcome messages
        self.log.add("Welcome to Chest Hunters!")
        self.log.add("Attack zombies to gain points, or collect points from chests.")
        self.log.add("Survive till the end of the wave to upgrade your stats!")

    # ----------------------------------------------------------------------
    # Scene interface
    # ----------------------------------------------------------------------

    def handle_events(self, events: List[pygame.event.Event]):
        for ev in events:
            if ev.type == pygame.VIDEORESIZE:
                # Handle resize for UI elements
                self.log.handle_resize(self.game.display_height)
                self.hud.handle_resize()
            elif not self.world.is_frozen and ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    self.player.handle_click(ev.pos[0], ev.pos[1])

        self.player.handle_input()

    def fixed_update(self, dt: float):
        if self.world.is_frozen:
            return
        min_x, min_y, max_x, max_y = get_screen_bounds(self.player, self.game)
        entities = self.world.get_entities_in_region(min_x, min_y, max_x, max_y)

        for ent in entities:
            ent.tick(dt)

        # Zombie spawning – deterministic, fixed-rate
        self._spawn_zombies()

        if self.wave_manager.get_current_wave() is not None:
            progress = self.wave_manager.get_current_progress()
            if self.wave_manager.current_wave_index is not None and progress is not None and progress >= 1.0:
                # Wave complete
                self.log.add(f"Wave {self.wave_manager.current_wave_index + 1} complete!")
                self.wave_manager.waves.append(self._make_wave(self.wave_manager.current_wave_index + 2))
                self.wave_manager.start_next_wave()
                if self.wave_manager.get_current_wave() is not None:
                    self.log.add(f"Wave {self.wave_manager.current_wave_index + 1} starting!")
                else:
                    self.log.add("All waves complete! You survived!")

    def update(self, dt: float):
        # Update UI elements
        self.hud.update()

    def render(self, screen: pygame.Surface, alpha: float):
        # Render world - UI is handled by ui_manager in main.py
        self.renderer.render()

    # ----------------------------------------------------------------------
    # Internal helpers
    # ----------------------------------------------------------------------

    def _generate_tiles(self):
        tile_map = self.world.get_tile_map()

        for x in range(-50, 50):
            for y in range(-50, 50):
                r = random.random()

                if (x + y) % 3 == 0:
                    tile_map.add_tile(x, y, DIRT)
                else:
                    tile_map.add_tile(x, y, GRASS)
                    if r < 0.1:
                        tree = Tree(x, y)
                        if not self.world.has_collision(tree):
                            tree.set_world(self.world)
                        else:
                            del tree

                if r < 0.005:
                    chest = Chest(x, y)
                    if not self.world.has_collision(chest):
                        chest.set_world(self.world)
                    else:
                        del chest

    def _spawn_zombies(self):
        current_wave = self.wave_manager.get_current_wave()
        if current_wave is None:
            return
        
        max_zombies = current_wave.max_zombies
        r = random.random()
        if len(self.world.get_entities_of_type(Zombie)) >= max_zombies:
            return

        if r < 0.2:  # Spawn chance per tick
            x = random.randint(-50, 50)
            y = random.randint(-50, 50)
            zombie = Zombie(x, y)
            zombie.health = random.randint(current_wave.min_zombie_health, current_wave.max_zombie_health)
            zombie.max_health = zombie.health
            if not self.world.has_collision(zombie):
                zombie.set_world(self.world)
            else:
                del zombie

    def _make_wave(self, wave_number: int) -> Wave:
        max_zombies = random.randint(5 + wave_number * 2, 10 + wave_number * 3)
        min_zombie_health = random.randint(10 + wave_number * 5, 20 + wave_number * 5)
        max_zombie_health = min_zombie_health + random.randint(0, 10 + wave_number * 5)
        min_zombie_strength = random.randint(1 + wave_number, 3 + wave_number)
        max_zombie_strength = min_zombie_strength + random.randint(0, 2 + wave_number)

        return Wave(
            max_zombies=max_zombies,
            min_zombie_health=min_zombie_health,
            max_zombie_health=max_zombie_health,
            min_zombie_strength=min_zombie_strength,
            max_zombie_strength=max_zombie_strength,
            spawn_interval_seconds=2.0 - min(1.5, wave_number * 0.1),
            wave_duration_seconds=60 + wave_number * 10
        )
