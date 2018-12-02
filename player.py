##!/usr/bin/env python

import pygame
import time
import math
from constants import *
from sprite_tools import *
from level import fp


class Player(object):

    def __init__(self, position):

        self.pos = position
        self.generate_control_enables()

        self.dash_mode = 0
        self.jump_mode = 0
        self.push_mode = 0

        idle_sprite = SpriteSheet(fp("keith.png"), (1, 1), 1)
        self.sprite = Sprite(8)
        self.sprite.scale = TILE_WIDTH*1.0/48
        self.sprite.add_animation({"idle": idle_sprite})
        self.sprite.start_animation("idle")

        self.sprite.x_pos = position[0] * TILE_WIDTH
        self.sprite.y_pos = position[1] * TILE_WIDTH - TILE_WIDTH

        self.hop_amp = TILE_WIDTH*1.0*.7
        self.hop_height = 0
        self.hop_enable = 0
        self.hop_time = 0
        self.hop_duration = 0.1

    def hop(self):
        self.hop_enable = 1
        self.hop_height = 0.001
        self.hop_time = 0

    def update_hop(self, dt):
        hop_rate = 12
        if self.hop_height <= 0:
            self.hop_enable = 0
            self.hop_height = 0
        elif self.hop_enable:
            self.hop_time += dt
            self.hop_height = self.hop_func(self.hop_time/self.hop_duration)

    def hop_func(self, prop_thru):
        atk = 15.0
        dec = 2.0
        return min((prop_thru*atk)**0.2, (1-prop_thru)*dec) * self.hop_amp

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

    def update(self, dt):
        self.update_sprite_position(dt)
        self.update_hop(dt)
        self.sprite.update(dt)

    def update_sprite_position(self, dt):
        dx = self.pos[0] * TILE_WIDTH - self.sprite.x_pos
        dy = self.pos[1] * TILE_WIDTH - self.sprite.y_pos - TILE_WIDTH - self.hop_height

        if dx+dy> TILE_WIDTH * 3:
            print("HERHERHERHE")
            self.sprite.x_pos = self.pos[0] * TILE_WIDTH
            self.sprite.y_pos = self.pos[1] * TILE_WIDTH
            return

        rate = 16
        self.sprite.x_pos += dx*rate*dt
        self.sprite.y_pos += dy*rate*dt


    def draw(self, surf):
        x = self.pos[0] * TILE_WIDTH
        y = self.pos[1] * TILE_WIDTH - self.hop_height

        # pygame.draw.rect(surf, (255, 255, 255),
        #     (x +TILE_WIDTH/8,
        #     y +TILE_WIDTH/8,
        #     TILE_WIDTH*3/4, TILE_WIDTH*3/4))

        #self.sprite.set_position((x, y-TILE_WIDTH))
        self.sprite.draw(surf)
