##!/usr/bin/env python

import pygame
from constants import *

class Goal(object):

    def __init__(self, pos):
        self.pos = pos

    def draw(self, surf):
        pos = self.pos
        pygame.draw.rect(surf, (140, 40, 160),
            (pos[0] * TILE_WIDTH+TILE_WIDTH/8,
            pos[1] * TILE_WIDTH+TILE_WIDTH/8,
            TILE_WIDTH*3/4, TILE_WIDTH*3/4))
