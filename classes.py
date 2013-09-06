# -*- coding: utf-8 -*-
import pygame
import datetime


class Score(object):
    def __init__(self, name, score):
        now = datetime.datetime.now()
        self.date = now.strftime("%Y-%m-%d %H:%M")
        self.name = name
        self.score = score


class Text(pygame.sprite.Sprite):
    def __init__(self, size, h=(255, 255, 0), n=(200, 200, 0)):
        pygame.sprite.Sprite.__init__(self)
        try:
            self.font = pygame.font.Font("fonts/kremlin.ttf", size)
        except:
            self.font = pygame.font.SysFont("Georgia", size)
        self.hoverc = h  # lime green, #c8f082 in hex
        self.normalc = n  # washed out green, #8c968c in hex


class Popup(Text):
    def __init__(self, x, y, image, text, size=30):
        super(Popup, self).__init__(size)
        pygame.sprite.Sprite.__init__(self)
        w, h = image.get_width(), image.get_height()
        self.rect = pygame.Rect(x, y, w, h)
        self.image = image
        try:
            self.font = pygame.font.Font("fonts/kremlin.ttf", size)
        except:
            self.font = pygame.font.SysFont("Georgia", size)
        font_w, font_h = self.font.size(text)
        label = self.font.render(text, True, self.normalc)
        self.image.blit(label, [w/2-font_w/2, h/2-font_h/2])
        self.text = text


class Title(Text):
    def __init__(self, x, text, c=(255, 255, 0), size=50):
        super(Title, self).__init__(size, n=c)
        w, h = self.font.size(text)
        x, y = x-w/2, 5
        self.rect = pygame.Rect(x, y, w, h)
        self.image = self.font.render(text, True, self.normalc)


class MenuItem(Text):
    def __init__(self, xy, text, action, size):
        super(MenuItem, self).__init__(size)
        from blocks import Blocks
        self.b = Blocks(size)
        self.action = action
        self.hovered = False
        self.text = text
        self.w, self.h = self.font.size(text)
        x, y = xy[0]-self.w/2, xy[1]
        self.rect = pygame.Rect(x, y, self.w, self.h)
        self.s = pygame.Surface((self.b.size*1.5+self.w, self.h),
                                pygame.SRCALPHA, 32)
        self.s.convert_alpha()
        self.image = self.font.render(self.text, True, self.normalc)
        self.s.blit(self.image, (self.b.size*1.5, 0))
        self.image = self.s

    def hover(self):
        self.s = pygame.Surface((self.b.size*1.5+self.w, self.h),
                                pygame.SRCALPHA, 32)
        self.s.convert_alpha()
        self.image = self.font.render(self.text, True, self.hoverc)
        self.s.blit(self.image, (self.b.size*1.5, 0))
        self.s.blit(self.b.b, (0, 0))
        self.image = self.s
        self.hovered = True

    def score(self, score):
        self.action += score
        textandscore = self.text
        textandscore += str(self.action)
        self.image = self.font.render(textandscore, True, self.normalc)

    def normal(self):
        self.s = pygame.Surface((self.b.size*1.5+self.w, self.h),
                                pygame.SRCALPHA, 32)
        self.s.convert_alpha()
        self.image = self.font.render(self.text, True, self.normalc)
        self.s.blit(self.image, (self.b.size*1.5, 0))
        self.image = self.s
        self.hovered = False


class MenuItemScore(MenuItem):
    def __init__(self, xy, score, size=30):
        text = score.name+": "+str(score.score)
        super(MenuItemScore, self).__init__(xy, text, "show_date", size)
        self.date = score.date
        self.name = score.name
        self.score = score.score
        self.dateshown = False

    def show(self):
        if self.dateshown:
            text = self.name+": "+str(self.score)
            self.image = self.font.render(text, True, self.hoverc)
            self.dateshown = False
        else:
            text = self.name+": "+str(self.date)
            self.image = self.font.render(text, True, self.hoverc)
            self.dateshown = True


class Input(Text):
    def __init__(self, rect, action, size=30, fps=5):
        super(Input, self).__init__(size)
        self.rect = rect
        self.data = ""
        self.w, self.h = self.rect.width, self.rect.height
        self.bg = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)
        self.bg.convert_alpha()
        self.bg.fill([200, 200, 0])
        self.bg.set_alpha(100)
        self.fbg = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)
        self.fbg.convert_alpha()
        self.fbg.fill([255, 255, 0])
        self.fbg.set_alpha(100)
        self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        self.image.blit(self.bg, (0, 0))
        self.hovered = False
        self.action = action
        self.normalc = (0, 0, 0)

        self._start = pygame.time.get_ticks()
        self._delay = 2000 / fps
        self._last_update = 0
        self._frame = 0

        self.update(pygame.time.get_ticks())

    def update(self, t):

        ndata = self.data
        if t - self._last_update > self._delay:

            if self._frame == 0:
                if self.hovered:

                    ndata += "|"
                    self._frame += 1
            else:
                self._frame -= 1
            text = self.font.render(ndata, True, self.normalc)
            if not self.hovered:
                self.image.blit(self.bg, (0, 0))
            else:
                self.image.blit(self.fbg, (0, 0))
            self.image.blit(text, (5, 5))
            self._last_update = t

    def normal(self):
        self.image.blit(self.bg, (0, 0))
        text = self.font.render(self.data, True, self.normalc)
        self.image.blit(text, (5, 5))
        self.hovered = False

    def hover(self):
        self.image.blit(self.fbg, (0, 0))
        text = self.font.render(self.data, True, self.normalc)
        self.image.blit(text, (5, 5))
        self.hovered = True

    def update_data(self, data, upper):
        if data == 8:  # backspace
            self.data = self.data[:-1]
        elif data <= 127 and len(self.data) <= 10:
            if upper:
                self.data += (chr(data)).upper()
            else:
                self.data += (chr(data))
        text = self.font.render(self.data, True, self.normalc)
        self.image.blit(self.fbg, (0, 0))
        self.image.blit(text, (5, 5))


class Wall(pygame.sprite.Sprite):
    """
    Walls used for collisions to keep tetrominos inside the game area.
    """
    def __init__(self, rect, color=""):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.image = pygame.Surface(
            (self.rect.width, self.rect.height),
            pygame.SRCALPHA, 32
        )
        if color is not "":
            self.image.fill(color)
        else:
            self.image.fill((0, 0, 0))
        self.image.convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)


class LockedTetrominos(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        w, h = image.get_width(), image.get_height()
        self.rect = pygame.Rect(x, y, w, h)
        self.mask = pygame.mask.from_surface(self.image)

    def combine(self, tetromino):
        """
        Tetromino gets blitted to the image of this class.
        """
        x, y = tetromino.rect.x, tetromino.rect.y
        self.image.blit(tetromino.image, (x-5, y-5))
        self.mask = pygame.mask.from_surface(self.image)

    def removerect(self, rect):
        """
        Remove a line of blocks and move everything above it down one block.
        """
        move = pygame.Rect(0, 0, rect.width, rect.top)
        sub = self.image.subsurface(move)
        subreal = sub.copy()
        self.image.fill((0), rect)
        self.image.fill((0), move)

        self.image.blit(
            subreal,
            (rect.left, rect.bottom-subreal.get_height())
        )
        self.mask = pygame.mask.from_surface(self.image)


class Tetromino(pygame.sprite.Sprite):
    def __init__(self, x, y, image, type, blocksize):
        pygame.sprite.Sprite.__init__(self)
        w, h = image.get_width(), image.get_height()
        self.image = image
        self.rect = pygame.Rect(x, y, w, h)
        self.type = type
        self.blocksize = blocksize
        self.mask = pygame.mask.from_surface(self.image)
        self.switched = False

    def update(self, direction=[0, 1]):
        self.rect.left += self.blocksize*direction[0]
        self.rect.bottom += self.blocksize*direction[1]

    def rotate(self, direction):
        if self.type != "O":
            self.image = pygame.transform.rotate(self.image, direction*90)
            self.mask = pygame.mask.from_surface(self.image)

    def switch(self, tetromino):
        oldtet = Tetromino(
            self.rect.width, self.rect.height, self.image,
            self.type, self.blocksize
        )

        w, h = tetromino.rect.width, tetromino.rect.height
        self.rect = pygame.Rect(self.rect.left, self.rect.top, w, h)
        self.image = tetromino.image
        self.mask = pygame.mask.from_surface(self.image)
        self.type = tetromino.type
        self.switched = True
        return oldtet
