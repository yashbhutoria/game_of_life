from game_of_life.life import GameOfLife, Canvas
from game_of_life.lives.oscillators import *
from game_of_life.lives.space_ships import *
from game_of_life.lives.still_lives import *
import pygame


SCREEN_SIZE = 1366, 768
screen = pygame.display.set_mode(SCREEN_SIZE)

canvas = Canvas(rows=SCREEN_SIZE[1] // 5, columns=SCREEN_SIZE[0] // 5)
canvas.add_life(life=GOSPELS_GLIDER_GUN, x=10, y=10)
game = GameOfLife(screen=screen, initial_state=canvas.get_canvas(), refresh_delay=0)

pygame.init()
game.start()
pygame.quit()