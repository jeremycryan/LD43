##!/usr/bin/env python
import pygame

WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT

TILE_WIDTH = 50

PIT = "."
FLOOR = ","
WALL = "W"
PLAYER = "P"
BLOCK = "B"
GOAL = "G"

SHRINES = ["S"]
DOORS = ["1"]

DOWN = 0
LEFT = 1
RIGHT = 2
UP = 3
DASH = 4
PUSH = 5
JUMP = 6
CONTROLS = {pygame.K_DOWN: DOWN,
    pygame.K_UP: UP,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT,
    pygame.K_z: DASH,
    pygame.K_x: PUSH,
    pygame.K_c: JUMP}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

HUD_KEY_Y = WINDOW_HEIGHT - 120
HUD_KEY_X = 40
HUD_KEY_ORDER = {
    DASH: 0,
    PUSH: 1,
    JUMP: 2,
    LEFT: 3,
    UP: 4,
    DOWN: 4,
    RIGHT: 5
}

HUD_KEY_WIDTH = 80
HUD_KEY_HEIGHT = 100
UP_OFFSET = HUD_KEY_HEIGHT+20

HUD_KEY_X_SPACING = 20
