##!/usr/bin/env python

import pygame
from constants import *

class Block(object):

    def __init__(self, pos):
        self.pos = pos

    def draw(self, surf):
        pos = self.pos
        pygame.draw.rect(surf, (130, 100, 70),
            (pos[0] * TILE_WIDTH+TILE_WIDTH/8,
            pos[1] * TILE_WIDTH+TILE_WIDTH/8,
            TILE_WIDTH*3/4, TILE_WIDTH*3/4))

    def move_target(self, direction, force_1 = False):
        dist = 1

        if direction == UP:
            target = self.pos[0], self.pos[1] - dist
        elif direction == DOWN:
            target = self.pos[0], self.pos[1] + dist
        elif direction == LEFT:
            target = self.pos[0] - dist, self.pos[1]
        elif direction == RIGHT:
            target = self.pos[0] + dist, self.pos[1]
        return target

    def move(self, direction, force_1 = False):

        dist = 1

        if direction == UP:
            self.pos = self.pos[0], self.pos[1] - dist
        elif direction == DOWN:
            self.pos = self.pos[0], self.pos[1] + dist
        elif direction == LEFT:
            self.pos = self.pos[0] - dist, self.pos[1]
        elif direction == RIGHT:
            self.pos = self.pos[0] + dist, self.pos[1]
