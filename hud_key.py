##!/usr/bin/env python

from constants import *

class HudKey(object):

    def __init__(self, key):

        self.key = key

        self.y = HUD_KEY_Y
        if key == UP:
            self.y -= UP_OFFSET
        self.start_y = self.y
        self.x = -100

        self.target_x, self.target_y = self.x, self.y

        self.enabled = True
        self.hover = False

        self.width = HUD_KEY_WIDTH
        self.height = HUD_KEY_HEIGHT
        self.scale = 1.0
        self.target_scale = 1.0

    def draw(self, surf):

        if self.hover:
            color = WHITE
        else:
            color = GRAY

        scale_diff = self.scale - 1
        scale_diff_half = scale_diff/2
        scale_offset_y = scale_diff_half * HUD_KEY_HEIGHT
        scale_offset_x = scale_diff_half * HUD_KEY_WIDTH
        pygame.draw.rect(surf, color,
            (self.x - scale_offset_x,
            self.y - scale_offset_y,
            self.width,
            self.height))


    def update(self, dt):

        rate = 8.0

        xdif = self.target_x - self.x
        self.x += (xdif * rate)*dt

        ydif = self.target_y - self.y
        self.y += (ydif * rate)*dt

        self.update_scale(dt)

    def update_scale(self, dt):
        scale_rate = 10.0
        ds = self.target_scale - self.scale
        self.scale += scale_rate * ds * dt

        self.width = HUD_KEY_WIDTH * self.scale
        self.height = HUD_KEY_HEIGHT * self.scale


    def mouse_over(self, mpos):
        mx, my = mpos
        if mx >= self.x and mx <= self.x + HUD_KEY_WIDTH:
            if my >= self.y and my <= self.y + HUD_KEY_HEIGHT:
                self.hover = True
                self.target_scale = 1.2
                return True
        self.target_scale = 1.0
        self.hover = False
        return False





class HudKeyArray(object):

    def __init__(self):

        self.keys = [UP, DOWN, LEFT, RIGHT, JUMP, PUSH, DASH]
        self.hud_keys = []
        for item in self.keys:
            self.hud_keys.append(HudKey(item))
        self.full_list = self.hud_keys

    def set_xs(self):

        priorities = [HUD_KEY_ORDER[key] for key in self.keys]
        priorities_un = list(set(priorities))

        for key in self.keys:
            priority = HUD_KEY_ORDER[key]
            x_index = priorities_un.index(priority)

            xcum = 0
            for item in self.hud_keys:
                if item.key == key:
                    item.target_x = x_index * (HUD_KEY_X_SPACING + HUD_KEY_WIDTH) + HUD_KEY_X

    def set_ys(self):

        for item in self.hud_keys:
            item.target_y = item.start_y

    def draw(self, surf):
        for key in self.hud_keys:
            key.draw(surf)

    def update(self, dt):
        self.set_xs()
        self.set_ys()
        for key in self.hud_keys:
            key.update(dt)

    def select_key(self, key):

        for item in self.hud_keys:
            if item.key == key:
                self.hud_keys.remove(item)

    def return_key(self, key):

        self.hud_keys.append(key)
