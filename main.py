#!/usr/bin/env python3

import curses
import random
import time
import math
from curses import wrapper
from util import *

log.info("////////////////////////////////")

FIREFLIES = 10
INCREMENT = 0.01    # this is the quantifier
BUMP = 0.01

fireflies = []


def main(screen):
    for x in range(FIREFLIES):
        fireflies.append(Firefly(random.random(), random.random(), random.random()))
    height, width = screen.getmaxyx()
    curses.curs_set(0)
    while True:        
        screen.clear()
        for firefly in fireflies:
            firefly.increment()
        for firefly in fireflies:
            if firefly.capacitor >= 1.0:
                firefly.flash()            
        for f, firefly in enumerate(fireflies):
            x, y = int(firefly.x * width), int(firefly.y * height)
            if firefly.lit:
                screen.addstr(y, x, str(firefly.id), curses.A_REVERSE)
            else:
                screen.addstr(y, x, str(firefly.id))
        screen.refresh()
        time.sleep(0.01)

class Firefly():

    last_id = 0

    def __init__(self, x, y, phase, frequency=1.0):
        self.id = Firefly.last_id
        Firefly.last_id += 1
        self.x = x
        self.y = y
        self.phase = phase
        self.frequency = frequency
        self.capacitor = self.f(self.phase)
        self.lit = False

    def increment(self):
        self.phase = min(self.phase + (INCREMENT * self.frequency), 1.0)
        self.capacitor = self.f(self.phase)

    def bump(self):
        log.info(f"--> {self.id} got bumped")
        self.capacitor = min(self.capacitor + BUMP, 1.0)
        self.phase = self.f_inv(self.capacitor)

    def flash(self):
        log.info(f"FLASH {self.id}")
        self.phase = 0.0
        self.capacitor = 0.0
        self.lit = not self.lit
        for firefly in fireflies:
            if firefly is self or firefly.lit:
                continue
            firefly.bump()        

    def f(self, x): # x is the phase
        return math.sin((math.pi / 2) * x)

    def f_inv(self, y): # y is the phase
        return (2 / math.pi) * math.asin(y)


wrapper(main)