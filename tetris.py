# -*- coding: utf-8 -*-
import pygame
import os
from menu import *


class Tetris(object):
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)  # sounds
        pygame.init()

        self.movekeys = {
            273: (0, 1),     # ups
            274: (0, -1),    # down
            275: (1, 0),     # right
            276: (-1, 0)     # left
        }

        self.width, self.height = 600, 600
        info = pygame.display.Info()           # get display info
        xpos = info.current_w/2-self.width/2   # get x position for corner
        ypos = info.current_h/2-self.height/2  # get y position for corner
        # display the game window at the center of the screen
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (xpos, ypos)
        pygame.display.set_mode((self.width, self.height))
        pygame.mouse.set_visible(False)
        pygame.display.set_caption("pyTetris")  # Set app name
        pygame.key.set_repeat(200, 80)  # delay, interval

    def main(self):
        menu = Menu(self.movekeys)
        while menu.main():
            pass

if __name__ == "__main__":
    tetris = Tetris()
    tetris.main()
