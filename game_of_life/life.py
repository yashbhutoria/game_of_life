import pygame
import threading
from pygame import Surface
from pygame.locals import QUIT
from time import sleep
import numpy as np
from scipy.ndimage import convolve


class GameOfLife:

    NEIGHBOUR_MASK = np.array(
        [
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1],
        ]
    )

    def rules(current_value: int, neighbour_count: int) -> int:
        # Any live cell with fewer than two live neighbours dies, as if by underpopulation.
        # Any live cell with more than three live neighbours dies, as if by overpopulation.
        # Any live cell with two or three live neighbours lives on to the next generation.
        # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        if (current_value == 1) and ((neighbour_count < 2) or (neighbour_count > 3)):
            return 0
        elif neighbour_count == 3:
            return 1
        return current_value

    v_apply_rule = np.vectorize(rules)

    def __init__(
        self, screen: Surface, initial_state: np.ndarray, refresh_delay: float = 0.1
    ) -> None:
        self._screen = screen
        self.state = initial_state
        self.screen_w, self.screen_h = screen.get_size()
        self.row, self.col = initial_state.shape
        self.refresh_delay = refresh_delay
        self.pixel_w = int(self.screen_w / self.col)
        self.pixel_h = int(self.screen_h / self.row)

    def draw_pixel(self, x: int, y: int) -> None:
        pygame.draw.rect(
            self._screen,
            (0, 255, 0),
            pygame.Rect(
                x * self.pixel_w,
                y * self.pixel_h,
                self.pixel_w,
                self.pixel_h,
            ),
        )

    def clear_screen(self) -> None:
        self._screen.fill((0, 0, 0))

    def render_state(self) -> None:
        for i, row in enumerate(self.state):
            for j, element in enumerate(row):
                if element == 1:
                    self.draw_pixel(j, i)
        pygame.display.flip()

    def calculate_next_state(self) -> None:
        neighbours_arr = convolve(self.state, self.NEIGHBOUR_MASK)
        self.state = self.v_apply_rule(self.state, neighbours_arr)

    def _display(self) -> None:
        while True:
            self.render_state()
            sleep(self.refresh_delay)
            self.clear_screen()
            self.calculate_next_state()

    def start(self) -> None:
        threading.Thread(target=self._display).start()

        while True:
            for evt in pygame.event.get():
                if evt.type == QUIT:
                    return


class Canvas:
    def __init__(self, rows: int, columns: int):
        self._canvas = np.ndarray((rows, columns))

    def add_life(self, life: np.ndarray, x: int, y: int) -> None:
        height, width = life.shape
        self._canvas[x : x + height, y : y + width] += life

    def get_canvas(self) -> np.ndarray:
        return self._canvas
