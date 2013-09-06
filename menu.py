# -*- coding: utf-8 -*-
import pygame
import cPickle
from musicplayer import *
from pygame.locals import *
from classes import *
from game import *


class Menu(object):
    def __init__(self, keys):
        self.movekeys = keys
        self.screen = pygame.display.get_surface()
        self.rect = self.screen.get_rect()
        self.menu = pygame.sprite.OrderedUpdates()
        self.background = pygame.Surface((self.rect.width, self.rect.height))
        self.background.fill((200, 0, 0))
        self.background.convert()
        self.theme = pygame.mixer.Sound("music/korobeininki.ogg")
        self.title = pygame.sprite.GroupSingle()
        self.fontsize = 30
        self.name = "Player1"

    def main(self):
        self.main_menu()

        self.theme.play(-1)
        while True:
            if self.input() is False:
                return False
            for button in self.menu:
                try:
                    tet = button.data
                    button.update(pygame.time.get_ticks())
                except:
                    pass
            self.draw()

    def input(self):
        for event in pygame.event.get():

            if event.type == QUIT:
                return False

            if event.type == KEYDOWN:
                if self.key_action(event.key) is False:
                    return False

            isinput = ""
            for button in self.menu:
                if button.action == "set_name":
                    isinput = button

            if isinput and event.type == KEYDOWN:
                if event.key is not K_RETURN:
                    mods = pygame.key.get_mods()
                    if (mods & KMOD_CAPS):
                        if (mods & KMOD_LSHIFT) or (mods & KMOD_RSHIFT):
                            isinput.update_data(event.key, False)
                        else:
                            isinput.update_data(event.key, True)
                    elif (mods & KMOD_LSHIFT) or (mods & KMOD_RSHIFT):
                        isinput.update_data(event.key, True)
                    elif event.key not in self.movekeys.keys():
                        isinput.update_data(event.key, False)
                else:
                    self.perform_action(isinput.action)

    def key_action(self, key):
        if key == K_RETURN:
            for button in self.menu:
                if button.action == "set_name" and button.hovered:
                    leave = False
                    button.normal()
                    for button in self.menu:
                        if button.action == "start_game":
                            button.hover()
                            leave = True
                    if leave:
                        break

                if button.hovered:
                    if self.perform_action(button.action) is False:
                        print "exit"
                        return False



        if key == K_ESCAPE:
            mainmenu = False
            for button in self.menu:
                if button.action == "exit":
                    button.hover()
                    mainmenu = True
                else:
                    button.normal()
            if not mainmenu:
                self.perform_action("main_menu")

        elif key in self.movekeys.keys():
            i = 0
            for button in self.menu:
                if button.hovered:
                    break
                i += 1
            if len(self.menu.sprites()) > 1:
                next = self.movekeys[key][1]
                if 0 <= i-next < len(self.menu.sprites()):
                    self.menu.sprites()[i].normal()
                    self.menu.sprites()[i-next].hover()

    def perform_action(self, name):
        function = getattr(self, name)
        if function() is False:
            return False

    def start_game(self):
        self.set_name()
        self.menu.empty()
        game = Game(self.name)
        game.main()
        self.main_menu()

    def set_name(self):
        for button in self.menu:
            if button.action == "set_name":
                self.name = button.data

    def show_date(self):
        for button in self.menu:
            if button.hovered:
                button.show()

    def highscore_menu(self):
        self.menu.empty()
        self.title.add(Title(self.screen.get_width()/2, "Highscores"))

        try:
            with open("highscore.dat"):
                pass
            self.savetable = cPickle.load(file("highscore.dat", "rb"))
        except:
            open("highscore.dat", "wb").close()
            self.savetable = []

        x, y = self.screen.get_width()/2, self.title.sprite.rect.height + 20
        fsize = int(self.fontsize-self.fontsize/3)
        if fsize % 2:
            fsize -= fsize % 2
        for score in self.savetable:
            self.menu.add(MenuItemScore((x-self.fontsize*1.5, y),
                                        score, size=fsize))
            y += self.fontsize+5

        y = y+self.fontsize*2+5

        back = MenuItem((x-self.fontsize*1.5, y), "Back", "main_menu",
                        self.fontsize)
        back.hover()
        self.menu.add(back)

    def name_menu(self):
        self.menu.empty()
        self.title.add(Title(self.screen.get_width()/2, "Insert name"))
        x = self.screen.get_width()/2
        y = self.title.sprite.rect.height + 20
        m = self.fontsize*5
        rect = pygame.Rect(x-m, y, self.fontsize*10, int(self.fontsize*1.5))
        name = Input(rect, "set_name")
        name.hover()
        self.menu.add(name)

        y = y + self.fontsize*2+5

        go = MenuItem((x-self.fontsize*1.5, y), "Start game", "start_game",
                      self.fontsize)
        self.menu.add(go)

        y = y + self.fontsize+5

        back = MenuItem((x-self.fontsize*1.5, y), "Back", "main_menu",
                        self.fontsize)
        self.menu.add(back)

    def options_menu(self):
        self.menu.empty()
        self.title.add(Title(self.screen.get_width()/2, "Options"))
        x = self.screen.get_width()/2
        y = self.title.sprite.rect.height + 20

        back = MenuItem((x-self.fontsize*1.5, y), "Back", "main_menu",
                        self.fontsize)
        back.hover()
        self.menu.add(back)

    def main_menu(self):
        self.menu.empty()
        self.title.add(Title(self.screen.get_width()/2, "Main menu"))
        y = self.title.sprite.rect.height + 20
        x = self.screen.get_width()/2

        start = MenuItem((x-self.fontsize*1.5, y), "Start game", "name_menu",
                         self.fontsize)
        start.hover()
        self.menu.add(start)

        y = y + self.fontsize + 5
        self.menu.add(MenuItem((x-self.fontsize*1.5, y), "Highscore",
                               "highscore_menu", self.fontsize))

        y = y + self.fontsize + 5
        self.menu.add(MenuItem((x-self.fontsize*1.5, y), "Options",
                               "options_menu", self.fontsize))

        y = y + self.fontsize + 5
        self.menu.add(MenuItem((x-self.fontsize*1.5, y), "Exit", "exit",
                               self.fontsize))

    def exit(self):
        return False

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.menu.draw(self.screen)
        self.title.draw(self.screen)
        pygame.display.update()
