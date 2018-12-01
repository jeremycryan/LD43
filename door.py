##!/usr/bin/env python
from constants import *
import pygame

class Door(object):

    def __init__(self, pos, shrine):

        self.shrine = shrine
        self.pos = pos

        self.width = TILE_WIDTH
        self.height = TILE_WIDTH

    def draw(self, surf):
        pos = self.pos

        color = (80, 80, 160)
        if self.is_passable():
            color = (120, 160, 180)

        pygame.draw.rect(surf, color,
            (pos[0] * TILE_WIDTH,
            pos[1] * TILE_WIDTH,
            self.width,
            self.height))

    def is_passable(self):
        return self.shrine.is_activated()
