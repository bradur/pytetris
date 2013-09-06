# -*- coding: utf-8 -*-
import pygame
from loaders import *


class MusicPlayer(object):

    def __init__(self, song=""):

        self.songend = pygame.USEREVENT + 1  # Whenever a track ends..
        self.tracknumber = 0
        if song:
            self.musiclist = [song]
        else:
            self.musiclist = load_files("music", ".ogg")   # another one
        load_music(self.musiclist[self.tracknumber])   # is loaded
        pygame.mixer.music.set_endevent(self.songend)  # and added
        if len(self.musiclist) > 1:
            self.tracknumber += 1                      # to the queue
        pygame.mixer.music.queue("music/"+self.musiclist[self.tracknumber])

    def next(self):
        if pygame.event.peek(self.songend):
            self.tracknumber += 1
            if self.tracknumber+1 >= len(self.musiclist):
                self.tracknumber = 0
                track = "music/"+self.musiclist[self.tracknumber]
                pygame.mixer.music.queue(track)
            else:
                track = "music/"+self.musiclist[self.tracknumber+1]
                pygame.mixer.music.queue(track)
