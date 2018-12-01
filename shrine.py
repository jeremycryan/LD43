##!/usr/bin/env python

from constants import *
import pygame

class Shrine(object):

    def __init__(self, pos, num=0):
        self.pos = pos

        self.num = num

        self.width = TILE_WIDTH
        self.height = TILE_WIDTH

        self.captured_key = []

    def is_activated(self):
        return len(self.captured_key) > 0

    def draw(self, surf):
        pos = self.pos
        pygame.draw.rect(surf, (255, 0, 0),
            (pos[0] * TILE_WIDTH,
            pos[1] * TILE_WIDTH,
            self.width,
            self.height))

        if len(self.captured_key):
            key = self.captured_key[0]
            key.x = pos[0] * TILE_WIDTH - HUD_KEY_WIDTH/2.0 + self.width/2
            key.y = pos[1] * TILE_WIDTH - key.height
            key.draw(surf)

    def update(self, dt):
        for key in self.captured_key:
            key.update_scale(dt)
