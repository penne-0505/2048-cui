"""
Animation system for the 2048-CLI game.
Provides smooth animations for tile movement, merging, and spawning.
"""

import threading
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any


class AnimationType(Enum):
    """Types of animations supported."""

    MOVE = "move"
    MERGE = "merge"
    SPAWN = "spawn"
    SCORE = "score"


@dataclass
class Position:
    """2D position with floating point precision."""

    x: float
    y: float

    def __add__(self, other: "Position") -> "Position":
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Position") -> "Position":
        return Position(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Position":
        return Position(self.x * scalar, self.y * scalar)


@dataclass
class TileAnimation:
    """Represents a single tile animation."""

    tile_id: str
    animation_type: AnimationType
    start_pos: Position
    end_pos: Position
    start_time: float
    duration: float
    value: int
    start_value: int | None = None  # For merge animations
    scale: float = 1.0  # For scale animations
    alpha: float = 1.0  # For fade animations

    @property
    def progress(self) -> float:
        """Get animation progress (0.0 to 1.0)."""
        elapsed = time.time() - self.start_time
        return min(1.0, max(0.0, elapsed / self.duration))

    @property
    def is_finished(self) -> bool:
        """Check if animation is complete."""
        return self.progress >= 1.0

    def get_current_position(self) -> Position:
        """Get current interpolated position."""
        if self.animation_type == AnimationType.MOVE:
            return self._ease_out_cubic(self.start_pos, self.end_pos, self.progress)
        return self.start_pos

    def get_current_scale(self) -> float:
        """Get current scale for merge animations."""
        if self.animation_type == AnimationType.MERGE:
            # Bounce effect: shrink then grow
            if self.progress < 0.5:
                # Shrink phase
                return 1.0 - (self.progress * 0.3)
            else:
                # Grow phase
                return 0.7 + ((self.progress - 0.5) * 0.6)
        elif self.animation_type == AnimationType.SPAWN:
            # Grow from 0 to 1
            return self._ease_out_back(0.0, 1.0, self.progress)
        return 1.0

    def get_current_alpha(self) -> float:
        """Get current alpha for fade animations."""
        if self.animation_type == AnimationType.SPAWN:
            return self._ease_out_cubic_scalar(0.0, 1.0, self.progress)
        return 1.0

    def _ease_out_cubic(self, start: Position, end: Position, t: float) -> Position:
        """Cubic ease-out interpolation for smooth movement."""
        eased_t = 1 - pow(1 - t, 3)
        diff = end - start
        return start + (diff * eased_t)

    def _ease_out_cubic_scalar(self, start: float, end: float, t: float) -> float:
        """Cubic ease-out interpolation for scalar values."""
        eased_t = 1 - pow(1 - t, 3)
        return start + (end - start) * eased_t

    def _ease_out_back(self, start: float, end: float, t: float) -> float:
        """Back ease-out for bounce effect."""
        c1 = 1.70158
        c3 = c1 + 1
        eased_t = 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)
        return start + (end - start) * eased_t


class AnimationManager:
    """Manages all game animations."""

    def __init__(self, board_size: int = 4):
        self.board_size = board_size
        self.active_animations: list[TileAnimation] = []
        self.running = False
        self.fps = 60
        self.speed_multiplier = 1.0
        self._render_thread: threading.Thread | None = None
        self._lock = threading.Lock()

        # Animation durations (in seconds)
        self.move_duration = 0.3
        self.merge_duration = 0.2
        self.spawn_duration = 0.15

        # Tile positions cache for drawing
        self.tile_positions: dict[str, Position] = {}
        self.tile_scales: dict[str, float] = {}
        self.tile_alphas: dict[str, float] = {}

    def set_fps(self, fps: int) -> None:
        """Set animation frame rate."""
        self.fps = max(30, min(120, fps))

    def set_speed_multiplier(self, speed: float) -> None:
        """Set animation speed multiplier."""
        self.speed_multiplier = max(0.5, min(2.0, speed))

    def start(self) -> None:
        """Start the animation manager."""
        if not self.running:
            self.running = True
            self._render_thread = threading.Thread(
                target=self._animation_loop, daemon=True
            )
            self._render_thread.start()

    def stop(self) -> None:
        """Stop the animation manager."""
        self.running = False
        if self._render_thread:
            self._render_thread.join(timeout=1.0)

    def add_move_animation(
        self,
        tile_id: str,
        from_pos: tuple[int, int],
        to_pos: tuple[int, int],
        value: int,
    ) -> None:
        """Add a tile movement animation."""
        start_pos = Position(float(from_pos[1]), float(from_pos[0]))
        end_pos = Position(float(to_pos[1]), float(to_pos[0]))

        animation = TileAnimation(
            tile_id=tile_id,
            animation_type=AnimationType.MOVE,
            start_pos=start_pos,
            end_pos=end_pos,
            start_time=time.time(),
            duration=self.move_duration / self.speed_multiplier,
            value=value,
        )

        with self._lock:
            self.active_animations.append(animation)

    def add_merge_animation(
        self, tile_id: str, pos: tuple[int, int], old_value: int, new_value: int
    ) -> None:
        """Add a tile merge animation."""
        position = Position(float(pos[1]), float(pos[0]))

        animation = TileAnimation(
            tile_id=tile_id,
            animation_type=AnimationType.MERGE,
            start_pos=position,
            end_pos=position,
            start_time=time.time(),
            duration=self.merge_duration / self.speed_multiplier,
            value=new_value,
            start_value=old_value,
        )

        with self._lock:
            self.active_animations.append(animation)

    def add_spawn_animation(
        self, tile_id: str, pos: tuple[int, int], value: int
    ) -> None:
        """Add a new tile spawn animation."""
        position = Position(float(pos[1]), float(pos[0]))

        animation = TileAnimation(
            tile_id=tile_id,
            animation_type=AnimationType.SPAWN,
            start_pos=position,
            end_pos=position,
            start_time=time.time(),
            duration=self.spawn_duration / self.speed_multiplier,
            value=value,
        )

        with self._lock:
            self.active_animations.append(animation)

    def has_active_animations(self) -> bool:
        """Check if there are any active animations."""
        with self._lock:
            return len(self.active_animations) > 0

    def skip_all_animations(self) -> None:
        """Skip all current animations to their end state."""
        with self._lock:
            for animation in self.active_animations:
                # Force animation to completion
                animation.start_time = time.time() - animation.duration
            self._update_positions()
            self.active_animations.clear()

    def get_tile_render_data(self, tile_id: str) -> dict[str, Any] | None:
        """Get current rendering data for a tile."""
        with self._lock:
            if tile_id in self.tile_positions:
                return {
                    "position": self.tile_positions[tile_id],
                    "scale": self.tile_scales.get(tile_id, 1.0),
                    "alpha": self.tile_alphas.get(tile_id, 1.0),
                }
        return None

    def _animation_loop(self) -> None:
        """Main animation loop running in separate thread."""
        frame_time = 1.0 / self.fps

        while self.running:
            loop_start = time.time()

            with self._lock:
                self._update_animations()

            # Frame rate control
            elapsed = time.time() - loop_start
            sleep_time = max(0, frame_time - elapsed)
            time.sleep(sleep_time)

    def _update_animations(self) -> None:
        """Update all active animations."""
        current_time = time.time()
        finished_animations = []

        for animation in self.active_animations:
            if animation.is_finished:
                finished_animations.append(animation)
            else:
                # Update tile render data
                self.tile_positions[animation.tile_id] = (
                    animation.get_current_position()
                )
                self.tile_scales[animation.tile_id] = animation.get_current_scale()
                self.tile_alphas[animation.tile_id] = animation.get_current_alpha()

        # Remove finished animations
        for animation in finished_animations:
            self.active_animations.remove(animation)
            # Set final state
            self.tile_positions[animation.tile_id] = animation.end_pos
            self.tile_scales[animation.tile_id] = 1.0
            self.tile_alphas[animation.tile_id] = 1.0

        self._update_positions()

    def _update_positions(self) -> None:
        """Update cached positions for all tiles."""
        # Clean up positions for animations that are no longer active
        active_tile_ids = {anim.tile_id for anim in self.active_animations}

        # Keep positions for tiles that might still be rendering
        for tile_id in list(self.tile_positions.keys()):
            if tile_id not in active_tile_ids:
                # Keep the final position but reset effects
                if tile_id in self.tile_scales:
                    self.tile_scales[tile_id] = 1.0
                if tile_id in self.tile_alphas:
                    self.tile_alphas[tile_id] = 1.0

    def clear_all_animations(self) -> None:
        """Clear all animations and reset state."""
        with self._lock:
            self.active_animations.clear()
            self.tile_positions.clear()
            self.tile_scales.clear()
            self.tile_alphas.clear()
