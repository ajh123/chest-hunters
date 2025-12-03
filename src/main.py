from __future__ import annotations
import pygame
from scenes import Scene
from scenes.menu_scene import MenuScene

class Game:
    def __init__(self, width: int = 800, height: int = 600):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.display_width = width
        self.display_height = height
        self.clock = pygame.time.Clock()
        self.running = True

        # fixed-step timing (global)
        self.fixed_dt = 1.0 / 60.0
        self.accumulator = 0.0
        self.last_time = pygame.time.get_ticks() / 1000.0

        # scene management
        self.current_scene: Scene = MenuScene(self)

    def set_scene(self, scene: Scene):
        self.current_scene = scene

    def _gather_events(self) -> list[pygame.event.Event]:
        return list(pygame.event.get())

    def run(self):
        while self.running:
            events = self._gather_events()
            for ev in events:
                if ev.type == pygame.QUIT:
                    self.running = False

                elif ev.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((ev.w, ev.h), pygame.RESIZABLE)
                    self.display_width = ev.w
                    self.display_height = ev.h

            # deliver raw events to scene first (scene may change state / switch)
            self.current_scene.handle_events(events)

            # --- timing: frame / fixed-step management (single global place) ---
            now = pygame.time.get_ticks() / 1000.0
            frame_time = now - self.last_time
            self.last_time = now

            # clamp to avoid spiral of death
            if frame_time > 0.25:
                frame_time = 0.25

            self.accumulator += frame_time

            # run fixed steps
            while self.accumulator >= self.fixed_dt:
                # deterministic updates
                self.current_scene.fixed_update(self.fixed_dt)
                self.accumulator -= self.fixed_dt

            # compute alpha for render interpolation (0..1)
            alpha = self.accumulator / self.fixed_dt if self.fixed_dt > 0 else 1.0

            # per-frame update (non-critical)
            dt = self.clock.get_time() / 1000.0
            self.current_scene.update(dt)

            # render with interpolation
            self.current_scene.render(self.screen, alpha)

            # cap frame rate
            self.clock.tick(120)

        pygame.quit()

if __name__ == "__main__":
    game = Game(800, 600)
    game.run()