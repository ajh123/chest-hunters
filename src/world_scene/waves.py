from typing import List
from dataclasses import dataclass
import time


@dataclass
class Wave:
    max_zombies: int
    min_zombie_health: int
    max_zombie_health: int
    min_zombie_strength: int
    max_zombie_strength: int
    spawn_interval_seconds: float
    wave_duration_seconds: int


class WaveManager:
    def __init__(self, starting_wave: Wave):
        self.waves: List[Wave] = [starting_wave]
        self.current_wave_index: int | None = None
        self.current_start_time: float | None = None

    def add_wave(self, wave: Wave):
        self.waves.append(wave)

    def start_next_wave(self):
        if self.current_wave_index is None:
            self.current_wave_index = 0
        else:
            self.current_wave_index += 1

        if self.current_wave_index < len(self.waves):
            self.current_start_time = time.time()
        else:
            self.current_wave_index = None  # No more waves

    def get_current_wave(self) -> Wave | None:
        if self.current_wave_index is not None:
            return self.waves[self.current_wave_index]
        return None
    
    def get_current_progress(self) -> float | None:
        if self.current_wave_index is not None and self.current_start_time is not None:
            elapsed_time = time.time() - self.current_start_time
            current_wave = self.waves[self.current_wave_index]
            return min(elapsed_time / current_wave.wave_duration_seconds, 1.0)
        return None
