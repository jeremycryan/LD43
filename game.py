##!/usr/bin/env python
import pygame
import time
from level import Level
from constants import *
from camera_tools import Camera
from player import Player
from goal import Goal
from block import Block
from hud_key import *
from shrine import *
from door import *

class Game():

    def __init__(self):
        pygame.init()
        self.screen_commit = pygame.display.set_mode((1600, 900))
        self.screen = pygame.Surface((1600, 900))

        self.cam = Camera(self.screen_commit)
        self.cam.set_pan_pid(6, 2, -0.2)

        self.levels = [Level("level_4.txt")]

        self.main()


    def main(self):
        for level in self.levels:
            self.run_level(level)


    def run_level(self, level_obj):

        self.hud_key_array = HudKeyArray()

        self.clicked = 0
        self.selected_key = []
        self.hovered_shrine = []

        self.cur_level = level_obj

        then = time.time()
        self.cam.set_target_center(level_obj.surf_half)

        self.player_pos = level_obj.player_start_pos()
        self.player = Player(self.player_pos)
        self.goal = Goal(level_obj.goal_pos())
        self.blocks = []
        for item in level_obj.block_pos():
            self.blocks.append(Block(item))

        self.shrines = []
        self.doors = []
        if self.cur_level.shrine_count > 0:
            self.shrine_0 = Shrine(self.cur_level.shrine_0_pos(), num=0)
            self.door_0 = Door(self.cur_level.door_0_pos(), self.shrine_0)
        self.shrines.append(self.shrine_0)
        self.doors.append(self.door_0)

        while True:

            now = time.time()
            dt = now - then
            then = now
            dt = self.cam.time_step(dt)

            self.test_keydowns()

            level_obj.draw_level(self.screen)
            for block in self.blocks:
                block.draw(self.screen)
            self.shrine_0.draw(self.screen)
            self.door_0.draw(self.screen)
            self.goal.draw(self.screen)
            self.player.draw(self.screen)
            self.cam.capture(self.screen)

            self.draw_tools(self.screen_commit)

            self.update_objects(dt)
            self.mouse_triggers()

            pygame.display.flip()

    def can_move_here(self, pos, block=False):

        if self.unpassable_door_here(pos):
            return False

        block_poses = [item.pos for item in self.blocks]

        if self.cur_level.can_move_here(pos, block):
            if pos not in block_poses:
                return True

        if self.cur_level.pit_here(pos) and pos in block_poses:
            return True

        return False

    def unpassable_door_here(self, pos):

        for item in self.doors:
            if item.pos == pos:
                if not item.is_passable():
                    return True


    def block_here(self, pos):
        block_poses = [item.pos for item in self.blocks]
        for item in block_poses:
            if item == pos:
                if not self.cur_level.pit_here(pos):
                    return True

        return False

    def test_keydowns(self):

        events = pygame.event.get()
        keydowns = self.player.get_keydowns(events)
        keyups = self.player.get_keyups(events)
        bad_keydowns = self.player.get_bad_keydowns(events)

        for item in keydowns:
            if item in [UP, DOWN, RIGHT, LEFT]:

                if not self.unpassable_door_here(self.player.move_target(item, force_1 = True)):
                    if not self.block_here(self.player.move_target(item, force_1=True)):
                        if self.can_move_here(self.player.move_target(item)):
                            self.player.move(item)
                        elif self.can_move_here(self.player.move_target(item, force_1=True)):
                            self.player.move(item, force_1=True)

                    elif self.player.push_mode:
                        for block in self.blocks:
                            if block.pos == self.player.move_target(item):
                                if self.can_move_here(block.move_target(item), block=True):
                                    block.move(item)
                                    self.player.move(item)

            if item == DASH:
                self.player.dash_mode = 1
            if item == JUMP:
                self.player.jump_mode = 1
            if item == PUSH:
                self.player.push_mode = 1

        for item in keyups:
            if item == DASH:
                self.player.dash_mode = 0
            if item == JUMP:
                self.player.jump_mode = 0
            if item == PUSH:
                self.player.push_mode = 0


    def update_objects(self, dt):
        self.hud_key_array.update(dt)
        if len(self.selected_key):
            self.selected_key[0].update(dt)
        for shrine in self.shrines:
            shrine.update(dt)

        cam_x = self.player.pos[0]*TILE_WIDTH
        cam_y = self.player.pos[1]*TILE_WIDTH
        self.cam.set_target_center((cam_x, cam_y))


    def draw_tools(self, surf):
        enabled = self.player.control_enables

        self.hud_key_array.draw(surf)
        if len(self.selected_key):
            self.selected_key[0].draw(surf)

    def mouse_triggers(self):


        clicked = pygame.mouse.get_pressed()[0]

        if not clicked and len(self.selected_key):
            if len(self.hovered_shrine):
                self.hovered_shrine[0].captured_key = [self.selected_key.pop()]
            else:
                self.hud_key_array.return_key(self.selected_key[0])
            self.selected_key = []

        self.hovered_shrine = []

        mpos = pygame.mouse.get_pos()
        mx = mpos[0]
        my = mpos[1]

        for key in self.hud_key_array.hud_keys:
            if key.mouse_over(mpos):
                if clicked:
                    if len(self.selected_key):
                        self.hud_key_array.return_key(self.selected_key[0])
                    self.hud_key_array.select_key(key.key)
                    self.selected_key = [key]

        if len(self.selected_key):
            key = self.selected_key[0]
            key.target_x = mx - HUD_KEY_WIDTH/2
            key.target_y = my - HUD_KEY_HEIGHT/2

            for item in self.shrines:
                x = item.pos[0] * TILE_WIDTH + -self.cam.pos[0] + WINDOW_WIDTH/2
                y = item.pos[1] * TILE_WIDTH + -self.cam.pos[1] + WINDOW_HEIGHT/2
                key.target_scale = 1.2
                if mx > x and mx < x + item.width:
                    if my > y and my < y + item.height:
                        key.target_scale = 0.5
                        self.hovered_shrine = [item]

        self.set_control_enables()

    def set_control_enables(self):
        self.player.reset_control_enables()

        for item in self.hud_key_array.hud_keys:
            for k in CONTROLS:
                if CONTROLS[k] == item.key:
                    self.player.control_enables[k] = 1





if __name__ == '__main__':
    a = Game()
