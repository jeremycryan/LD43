##!/usr/bin/env python
import numpy as np
import pygame
from constants import *

class Level(object):


    def __init__(self, path):
        source_file = open(path, 'r')
        self.raw = source_file.readlines()
        self.map = np.asarray(self.raw)
        self.map = [[item for item in line[:-1]] for line in self.map]

        self.width = len(self.map[0])
        self.height = len(self.map)
        self.surf_width = self.width * TILE_WIDTH
        self.surf_height = self.height * TILE_WIDTH
        self.surf_half = [self.surf_width/2, self.surf_height/2]


    def player_start_pos(self):
        for (y, row) in enumerate(self.map):
            for (x, key) in enumerate(row):
                if key == PLAYER:
                    return (x, y)

    def goal_pos(self):
        for (y, row) in enumerate(self.map):
            for (x, key) in enumerate(row):
                if key == GOAL:
                    return (x, y)

    def block_pos(self):
        blocks = []
        for (y, row) in enumerate(self.map):
            for (x, key) in enumerate(row):
                if key == BLOCK:
                    blocks.append( (x, y) )
        return blocks

    def shrine_0_pos(self):
        for (y, row) in enumerate(self.map):
            for (x, key) in enumerate(row):
                if key == SHRINES[0]:
                    return (x, y)

    def door_0_pos(self):
        for (y, row) in enumerate(self.map):
            for (x, key) in enumerate(row):
                if key == DOORS[0]:
                    return (x, y)

    def shrine_count(self):
        i = 0
        for (y, row) in enumerate(self.map):
            for (x, key) in enumerate(row):
                if key in SHRINES:
                    i += 1
        return i


    def draw_tile(self, tile_key, position, surf):

        if tile_key in [FLOOR, PLAYER, BLOCK, GOAL] or tile_key in SHRINES or tile_key in DOORS:
            pygame.draw.rect(surf, (180, 170, 90), (position[0], position[1], TILE_WIDTH, TILE_WIDTH))
        elif tile_key == PIT:
            pygame.draw.rect(surf, (40, 40, 40), (position[0], position[1], TILE_WIDTH, TILE_WIDTH))
        elif tile_key == WALL:
            pygame.draw.rect(surf, (70, 140, 70), (position[0], position[1], TILE_WIDTH, TILE_WIDTH))
        elif tile_key == ELEVATED:
            pygame.draw.rect(surf, (160, 150, 80), (position[0], position[1], TILE_WIDTH, TILE_WIDTH))
        else:
            print(tile_key)

    def draw_level(self, surf):

        for (y, row) in enumerate(self.map):
            y_pos = y*TILE_WIDTH

            for (x, tile) in enumerate(row):
                x_pos = x*TILE_WIDTH

                self.draw_tile(tile, (x_pos, y_pos), surf)

    def can_move_here(self, pos, block=False, prev_pos = (0, 0), hop = False):
        prev = self.map[prev_pos[1]][prev_pos[0]]
        target = self.map[pos[1]][pos[0]]
        dist = abs(prev_pos[0] - pos[0]) + abs(prev_pos[1] - pos[1])

        if target in [PLAYER, FLOOR, GOAL, BLOCK] + DOORS:
            return True
        elif block and target == PIT:
            return True
        elif prev == ELEVATED and target == ELEVATED:
            return True
        elif target == ELEVATED and dist <= 1 and hop:
            return True
        else:
            return False

    def block_here(self, pos):
        target = self.map[pos[1]][pos[0]]
        if target in [BLOCK]:
            return True
        else:
            return False

    def pit_here(self, pos):
        target = self.map[pos[1]][pos[0]]
        if target in [PIT]:
            return True
        else:
            return False



if __name__ == '__main__':
    a = Level("level_1.txt")

    pygame.init()
    screen_commit = pygame.display.set_mode((1600, 900))

    a.draw_level(screen_commit)
    pygame.display.flip()

    while True:
        pass
