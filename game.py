# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from blocks import *
from classes import *
import random
import cPickle


class Game(object):
    def __init__(self, name):

        self.fps = 60
        self.name = name
        self.screen = pygame.display.get_surface()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.speed = 1000
        print self.name

        pygame.time.set_timer(USEREVENT+2, self.speed)

                                 # key name     ascii value
        self.movekeys = {
            K_a:     [-1, 0],    # a:           97
            K_d:     [1, 0],     # d:           100
            K_s:     [0, 1],     # s:           115
            K_RIGHT: [1, 0],     # right arrow: 275
            K_LEFT:  [-1, 0],    # left arrow:  276
            K_DOWN:  [0, 1]      # down arrow:  274
        }

        self.rotatekeys = {
            K_RCTRL: (1),        # right ctrl:  303
            K_LCTRL: (1),        # left ctrl:   304
            K_LSHIFT: (-1),      # left shift:  305
            K_RSHIFT: (-1)       # right shift: 306
        }

        # b is used when checking for filled lines
        self.b = pygame.sprite.GroupSingle()

        self.bsize = int((self.height-10)/20)
        self.fontsize = int(self.bsize*0.75)

        # create tetrominos using Blocks class
        self.blocks = Blocks(self.bsize)

        self.tetters = {
            "L": self.blocks.block_l,
            "I": self.blocks.block_i,
            "J": self.blocks.block_j,
            "O": self.blocks.block_o,
            "T": self.blocks.block_t,
            "S": self.blocks.block_s,
            "Z": self.blocks.block_z
        }

        self.tetrominos = self.tetters.keys()
        random.shuffle(self.tetrominos)

        # the tetromino that is currently in use
        self.tetromino = pygame.sprite.GroupSingle()

        # the ghost tetromino that is
        self.ghost = pygame.sprite.GroupSingle()

        # the tetrominoes that have locked in place
        self.lockedtetters = pygame.sprite.GroupSingle()

        # give the lockedtetromino group a transparent surface the size of
        # the game area so that locked tetrominos can be added to it
        t = pygame.Surface(
            (self.bsize*10, self.bsize*20),
            pygame.SRCALPHA, 32
        )
        self.lockedtetters.add(LockedTetrominos(5, 5, t))

        # draw background
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill((200, 0, 0))
        self.background.convert()

        # draw background to the game area
        self.gamearea = pygame.Surface((10*self.bsize, 20*self.bsize))
        self.gamearea.fill((200, 200, 0))
        self.gamearea.convert()

        # add walls to the sides of the game area for collisions
        self.walls = pygame.sprite.Group()
        self.walls.add(Wall(pygame.Rect(4, 0, 1, self.height),
                            (170, 170, 170)))
        self.walls.add(Wall(
            pygame.Rect(self.bsize*10+5, 0, 1, self.height),
            (170, 170, 170)
        ))

        # add a wall to the top of the game area for collisions
        self.topwall = pygame.sprite.Group()
        self.topwall.add(Wall(
            pygame.Rect(0, 0, self.bsize*10+10, 1),
            (170, 255, 170)
        ))

        # add a wall to the bottom of the game area for collisions
        self.botwall = pygame.sprite.Group()
        self.botwall.add(Wall(
            pygame.Rect(0, self.bsize*20+5, self.bsize*10+10, 1),
            (170, 170, 170)
        ))

        # sprite group for upcoming tetrominoes
        self.peek = pygame.sprite.OrderedUpdates()

        # sound that plays when player tries to do an illegal move
        self.blocksound = pygame.mixer.Sound("sfx/block.wav")

        # score HUD element
        self.score = pygame.sprite.GroupSingle()
        size = self.width-5-self.bsize*3
        score = MenuItem([size, 5], "Score: ", 0, size=self.fontsize,)
        score.normalc = (255, 255, 0)
        # draw score number
        score.score(0)
        self.score.add(score)

        # popup shown when game ends or is paused
        self.popup = pygame.sprite.GroupSingle()
        popup = pygame.Surface((self.bsize*8, self.bsize*5))
        popup.convert_alpha()
        popup.fill((255, 0, 0))
        popup.set_alpha(133)  # make surface translucent (0-255)

        x = self.gamearea.get_width()/2-self.bsize*4+5
        y = self.gamearea.get_height()/2-self.bsize*4/2+5
        self.popup.add(Popup(
            x, y, popup, "Exit to main menu?",
            size=self.fontsize
        ))

        self.menu = pygame.sprite.OrderedUpdates()

        # sound that plays when player clears a line
        self.clearsound = pygame.mixer.Sound("sfx/clear.wav")

        # if game is paused
        self.paused = False

        # open highscore file

    def main(self):
        self.drop_tetromino()
        self.create_ghost()
        self.drop_ghost()
        while True:
            self.draw()
            if self.input() is False:
                self.add_high_score()
                return False
            pygame.time.Clock().tick(self.fps)

    def add_high_score(self):
        try:
            with open("highscore.dat"):
                pass
            self.savetable = cPickle.load(file("highscore.dat", "rb"))
        except IOError:
            open("highscore.dat", "wb").close()
            self.savetable = []
        s = self.score.sprite.action
        for score in reversed(self.savetable):
            if score.score < s:
                self.savetable.remove(score)
                self.savetable.append(Score(self.name, s))
                self.savetable.sort(key=lambda x: x.score, reverse=True)
                cPickle.dump(self.savetable, file("highscore.dat", "wb"))
                break

    def create_ghost(self):
        for g in self.tetromino:
            type = g.type
            image = g.image
            rect = g.rect.copy()
            x, y = rect.x, rect.y  # start from same position as real tetromino
        im = pygame.Surface((rect.width, rect.height))
        im.convert_alpha()
        im.set_colorkey((255, 255, 255))  # set white as transparent
        im.fill((255, 255, 255))  # fill surface with white
        im.set_alpha(80)  # make surface translucent (0-255)
        im.blit(image, (0, 0))  # blit tetromino to surface
        self.ghost.add(Tetromino(x, y, im, type, self.bsize))

    def drop_ghost(self):
        for t in self.tetromino:
            for g in self.ghost:
                g.rect = t.rect.copy()
        while True:
            if self.collisions(
                [self.lockedtetters, self.botwall],
                self.ghost.sprite
            ):
                self.ghost.update([0, -1])
                break
            self.ghost.update()

    def drop_tetromino(self):
        scoreadd = self.check_for_filled_lines()
        if scoreadd:
            for s in self.score:
                s.score(scoreadd*10*scoreadd)
                self.clearsound.play()
            if self.speed >= 200:
                self.speed -= 50
                pygame.time.set_timer(USEREVENT+2, self.speed)
                print self.speed
        if len(self.tetrominos) == 0:
            self.tetrominos = self.tetters.keys()
            random.shuffle(self.tetrominos)
        if self.peek:
            ty = self.peek.sprites()[0]
            self.peek.remove(ty)
            type = ty.type
            self.peek.update([0, -4])
            newt = self.tetrominos.pop(0)
            newi = self.tetters[newt]
            self.peek.add(Tetromino(
                self.gamearea.get_width()+10,
                5*3+self.bsize*4*2, newi, newt, self.bsize)
            )
        else:
            type = self.tetrominos.pop(0)
            i = 0
            while i < 3:
                t = self.tetrominos.pop(0)
                im = self.tetters[t]
                self.peek.add(Tetromino(
                    self.gamearea.get_width()+10, 5+(5*i)+self.bsize*4*i,
                    im, t, self.bsize)
                )
                i += 1

        if type == "I":
            x = self.bsize*3+5
        elif type == "O":
            x = self.bsize*4+5
        else:
            x = int(random.randrange(5, self.bsize*4, self.bsize))
        image = self.tetters[type]
        y = self.bsize*-2+5
        self.tetromino.add(Tetromino(x, y, image, type, self.bsize))
        if self.collisions([self.lockedtetters]):
            self.exit_menu()
            self.tetromino.empty()

    def collisions(self, groups=[], sprite=""):
        if sprite == "":
            sprite = self.tetromino.sprite
        if not groups:
            groups = [self.walls, self.botwall, self.lockedtetters]
        for group in groups:
            if sprite and group:
                if pygame.sprite.spritecollide(
                    sprite, group, False,
                    pygame.sprite.collide_mask
                ):
                    return True
        return False

    def unpause(self):
        self.paused = False

    def pause(self):
        self.paused = True
        self.menu.empty()
        x = self.gamearea.get_width()/2-self.bsize*4+10+self.bsize
        y = self.gamearea.get_height()/2-self.bsize*4/2+5+self.bsize*4-5
        yes = MenuItem([x-self.fontsize*0.5, y],
                       "Yes", "exit_game", self.fontsize)
        yes.normalc = (200, 200, 0)
        yes.hover()
        self.menu.add(yes)
        x = x+self.bsize*6
        no = MenuItem([x-self.fontsize*1.5, y], "No", "unpause", self.fontsize)
        no.normalc = (200, 200, 0)
        no.normal()
        self.menu.add(no)

    def exit_menu(self):
        self.paused = True
        self.menu.empty()
        x = self.gamearea.get_width()/2
        y = self.gamearea.get_height()/2-self.bsize*4/2+5+self.bsize*4-5
        ok = MenuItem([x-self.fontsize*1.5, y],
                      "Ok", "exit_game", self.fontsize)
        ok.normalc = (200, 200, 0)
        ok.hover()
        self.menu.add(ok)

    def exit_game(self):
        return False

    def perform_action(self, name):
        function = getattr(self, name)
        if function() is False:
            return False

    def input(self):
        for event in pygame.event.get():

            if (event.type == QUIT or
               (event.type == KEYDOWN and event.key == K_ESCAPE)):
                if not self.paused:
                    self.pause()
                else:
                    self.unpause()

            if not self.paused:
                if event.type == KEYDOWN:
                    if self.key_action(event.key) is False:
                        return False

                if event.type == USEREVENT+2:  # Tetromino fall
                    self.tetromino.update()
                    if self.collisions([self.lockedtetters, self.botwall]):
                        self.tetromino.update([0, -1])
                        for t in self.tetromino:
                            for l in self.lockedtetters:
                                l.combine(t)
                                if self.collisions([self.topwall]):
                                    self.exit_menu()
                        self.drop_tetromino()
                        self.create_ghost()
                        self.drop_ghost()

            if self.paused:
                if event.type == KEYDOWN:
                    if event.key in [K_LEFT, K_RIGHT, K_a, K_d]:
                        print event.key
                        i = 0
                        for button in self.menu:
                            if button.hovered:
                                break
                            i += 1
                        if len(self.menu.sprites()) > 1:
                            next = self.movekeys[event.key][0]*-1
                            if 0 <= i-next < len(self.menu.sprites()):
                                self.menu.sprites()[i].normal()
                                self.menu.sprites()[i-next].hover()
                    if event.key == K_RETURN:
                        for button in self.menu:
                            if button.hovered:
                                if self.perform_action(button.action) is False:
                                    return False

    def check_for_filled_lines(self, multiplier=0):
        multiplier = multiplier
        i = 20
        if self.lockedtetters:
            while i*self.bsize+5 >= 5:
                j = 0
                found = 0
                istep = i*self.bsize+5
                while j*self.bsize+5 <= self.gamearea.get_width():
                    step = j*self.bsize+5
                    self.b.add(Wall(pygame.Rect(
                        step, istep, self.bsize, self.bsize
                    )))
                    if self.collisions([self.lockedtetters], self.b.sprite):
                        found += 1
                    j += 1
                if found == 10:
                    for l in self.lockedtetters:
                        rect = pygame.Rect(
                            0, i*self.bsize,
                            j*self.bsize,
                            self.bsize
                        )
                        multiplier += 1
                        l.removerect(rect)
                        multiplier = self.check_for_filled_lines(multiplier)
                i -= 1
        return multiplier

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.gamearea, (5, 5))
        self.ghost.draw(self.screen)
        self.tetromino.draw(self.screen)
        self.lockedtetters.draw(self.screen)
        #self.walls.draw(self.screen)
        self.peek.draw(self.screen)
        self.score.draw(self.screen)
        if self.paused:
            self.popup.draw(self.screen)
            self.menu.draw(self.screen)
        pygame.display.update()

    def key_action(self, key):
        if self.tetromino.sprite:
            if key == K_RETURN:  # enter key, ascii value 13
                for t in self.tetromino:
                    if not t.switched:
                        p = self.peek.sprites()[0]
                        s = p.switch(t)
                        t.switch(s)
                        if self.collisions():
                            self.blocksound.play()
                            s = p.switch(t)
                            t.switch(s)
                            t.switched = False
                        self.create_ghost()
                        self.drop_ghost()
                    else:
                        self.blocksound.play()

            if key == K_SPACE:  # space key, ascii value 32
                while True:
                    if self.collisions([self.lockedtetters, self.botwall]):
                        self.tetromino.update([0, -1])
                        for t in self.tetromino:
                            for l in self.lockedtetters:
                                l.combine(t)
                        self.drop_tetromino()
                        self.create_ghost()
                        self.drop_ghost()
                        break
                    self.tetromino.update()

            if key in self.movekeys.keys():
                self.tetromino.update(self.movekeys[key])
                if self.collisions():
                    new = self.movekeys[key][0]*-1, self.movekeys[key][1]*-1
                    self.tetromino.update(new)
                else:
                    self.drop_ghost()

            if key in self.rotatekeys.keys():
                for t in self.tetromino:
                    t.rotate(self.rotatekeys[key])
                    if self.collisions():
                        self.blocksound.play()
                        t.rotate(self.rotatekeys[key]*-1)
                    else:
                        self.create_ghost()
                        self.drop_ghost()
