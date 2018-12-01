##!/usr/bin/env python

import pygame
from constants import *


class Player(object):

    def __init__(self, position):

        self.pos = position
        self.generate_control_enables()

        self.dash_mode = 0
        self.jump_mode = 0
        self.push_mode = 0

    def generate_control_enables(self):
        self.control_enables = {}

        for key in CONTROLS:
            self.control_enables[key] = 1

    def reset_control_enables(self):
        self.control_enables = {}

        for key in CONTROLS:
            self.control_enables[key] = 0

    def move_target(self, direction, force_1 = False):
        dist = 1
        if self.dash_mode and not force_1:
            dist = 2

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
        if self.dash_mode and not force_1:
            dist = 2

        if direction == UP:
            self.pos = self.pos[0], self.pos[1] - dist
        elif direction == DOWN:
            self.pos = self.pos[0], self.pos[1] + dist
        elif direction == LEFT:
            self.pos = self.pos[0] - dist, self.pos[1]
        elif direction == RIGHT:
            self.pos = self.pos[0] + dist, self.pos[1]

    def get_pixel_pos(self):
        return (self.pos[0] * TILE_WIDTH,
            self.pos[1] * TILE_WIDTH)

    def get_keydowns(self, events):
        pressed = []
        for event in events:
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key in CONTROLS:
                    if self.control_enables[key]:
                        pressed.append(CONTROLS[key])
        return pressed

    def get_keyups(self, events):
        pressed = []
        for event in events:
            if event.type == pygame.KEYUP:
                key = event.key
                if key in CONTROLS:
                    if self.control_enables[key]:
                        pressed.append(CONTROLS[key])
        return pressed

    def get_bad_keydowns(self, events):
        pressed = []
        for event in events:
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key in CONTROLS:
                    if not self.control_enables[key]:
                        pressed.append(CONTROLS[key])
        return pressed

    def draw(self, surf):
        x = self.pos[0] * TILE_WIDTH
        y = self.pos[1] * TILE_WIDTH

        pygame.draw.rect(surf, (255, 255, 255),
            (x +TILE_WIDTH/8,
            y +TILE_WIDTH/8,
            TILE_WIDTH*3/4, TILE_WIDTH*3/4))
