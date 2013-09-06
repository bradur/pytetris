import os
import pygame
from pygame.locals import *


def load_image(img, colorkey=None, tp=False):  # Loads an image
    '''
    For loading and readying an image file.
    The parameter "tp" is for alpha transparency. It is off by default.
    The parameter "colorkey" is for color-based transparency.
    '''
    fullimg = os.path.join('img', img)
    try:
        image = pygame.image.load(fullimg)
    except pygame.error:
        print 'Cannot load image:', fullimg
    if tp is True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image


def load_music(musicfile):
    '''
    For loading and readying a music file
    '''
    class NoneMusic:
        def playmusic(self):
            pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneMusic()
    fullmusic = os.path.join('music', musicfile)
    try:
        music = pygame.mixer.music.load(fullmusic)
    except pygame.error:
        print 'Cannot load music file:', fullmusic
    return music


def load_files(path, extension):
    '''
    For loading all files of a certain type from a folder
    '''
    list_files = os.listdir(path)
    files = []
    for file in list_files:
        if file.endswith(extension):
            files.append(file)
    return files


def get_vorbis_info(filename):
    '''
    For parsing vorbis files
    '''
    comments = {}
    file = open("music/"+filename)
    data = file.read().split('vorbis')[2]  # Read in the file
    file.close()

    # Read in the length of the first field (vendor string)
    fieldLen = int(''.join([str(ord(c)) for c in data[3::-1]]))
    data = data[fieldLen+4:]  # Remove vendor string
    numComments = int(''.join([str(ord(c)) for c in data[3::-1]]))
    data = data[4:]  # Remove the comment field length data

    # Read in the comment fields
    for i in range(numComments):
        fieldLen = int(''.join([str(ord(c)) for c in data[3::-1]]))
        fieldData = data[4:fieldLen+4].split('=')
        comments[fieldData[0]] = fieldData[1]
        data = data[fieldLen+4:]

    return comments
