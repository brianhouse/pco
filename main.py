#!/usr/bin/env python3

import curses
import random
import time
import math
import threading
from curses import wrapper
from util import *

log.info("////////////////////////////////")

FIREFLIES = 30
FRAMERATE = 0.01
INCREMENT = 0.01    # this is the quantifier
BUMP = 0.02
RECOVERY = 5

fireflies = []

def main(screen):
    for x in range(FIREFLIES):
        fireflies.append(Firefly(random.random(), random.random(), random.random()))
    height, width = screen.getmaxyx()
    curses.curs_set(0)
    while True:        
        screen.clear()

        try:
            # spatial version
            # for f, firefly in enumerate(fireflies):
            #     x, y = int(firefly.x * width), int(firefly.y * height)
            #     if firefly.lit:
            #         screen.addstr(y, x, str(firefly.id), curses.A_REVERSE)
            #     else:
            #         screen.addstr(y, x, str(firefly.id))

            # phase display version
            for f, firefly in enumerate(fireflies):
                x = firefly.id * 2
                y = height - int(firefly.phase * (height - 1)) - 1
                screen.addstr(y, x, " ", curses.A_REVERSE)                               
        except Exception as e:
            log.error(e)

        screen.refresh()
        time.sleep(0.01)


class Firefly(threading.Thread):

    last_id = 0

    def __init__(self, x, y, phase, frequency=1.0):
        threading.Thread.__init__(self, daemon=True)
        self.id = Firefly.last_id
        Firefly.last_id += 1
        self.x = x
        self.y = y
        self.frequency = frequency
        self.phase = phase
        self.capacitor = self.f(self.phase)
        self.recovery = 0.0
        self.start()

    def run(self):
        while True:
            self.increment()
            time.sleep(FRAMERATE)

    def increment(self):
        try:
            self.phase = min(self.phase + (INCREMENT * self.frequency), 1.0)
            self.capacitor = self.f(self.phase)
            if self.recovery > 0:
                self.recovery -= 1
            if self.capacitor >= 1.0:
                self.fire()             
        except Exception as e:
            log.error(e)

    def bump(self):
        if not self.recovery:
            log.info(f"--> {self.id} got bumped")
            self.capacitor = min(self.capacitor + BUMP, 1.0)
            self.phase = self.f_inv(self.capacitor)
            if self.capacitor >= 1.0:
                self.fire()             

    def fire(self):
        log.info(f"FIRE {self.id}")
        self.phase = 0.0
        self.capacitor = 0.0
        self.recovery = RECOVERY
        for firefly in fireflies:
            if firefly is self:
                continue
            firefly.bump()        

    def f(self, x): # x is the phase
        return math.sin((math.pi / 2) * x)

    def f_inv(self, y): # y is the phase
        return (2 / math.pi) * math.asin(y)


wrapper(main)



'''

ok, so the effect I'm seeing is precisely right -- how to get rid of that

'''