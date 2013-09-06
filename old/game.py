# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *


class Game(object):
    def __init__(self, keys):
        self.fps = 60
        self.movekeys = keys
        self.screen = pygame.display.get_surface()
        self.rect = self.screen.get_rect()
        self.background = pygame.Surface((self.rect.width, self.rect.height))
        self.background.fill((170, 170, 170))
        self.background.convert()
        w = self.rect.width
        h = self.rect.height
        blocksize = (h-10.0)/20
        self.gamearea = pygame.Surface((10*blocksize, h-10))
        self.gamearea.fill((255, 255, 255))
        self.gamearea.convert()
        pygame.time.set_timer(USEREVENT+1, 5000)

    def main(self):
        while True:
            self.input()
            self.logic()
            self.draw()
            pygame.time.Clock().tick(self.fps)

    def pause(self):
        pass

    def key_action(self, key):
        if key == K_ESCAPE:
            self.pause()
            self.exit_menu()

        if key in self.movekeys.keys():
            pass

    def logic(self):
        pass

    def drop_tetromino(self):
        print "tet"

    def input(self):
        for event in pygame.event.get():

            if event.type == QUIT:
                self.pause()
                self.exit_menu()

            if event.type == KEYDOWN:
                if self.key_action(event.key) is False:
                    return False

            if event.type == USEREVENT+1:
                self.drop_tetromino()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.gamearea, (5, 5))

        pygame.display.update()
