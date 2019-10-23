#!/usr/bin/env python3

import curses
import random
import time
import math
import threading
from curses import wrapper
from util import *

log.info("////////////////////////////////")


FIREFLIES = 50

# percent of phase
BUMP = 1/100
RECOVERY = 20/100

# of display
FRAMERATE = 1/24

fireflies = []

def main(screen):
    for x in range(FIREFLIES):
        fireflies.append(Firefly(random.random(), random.random(), random.random()))
    height, width = screen.getmaxyx()
    curses.curs_set(0)
    while True:        
        screen.clear()
        try:
            # # spatial version
            # for f, firefly in enumerate(fireflies):
            #     x, y = int(firefly.x * width), int(firefly.y * height)
            #     if firefly.phase > 0.5:
            #         screen.addstr(y, x, str(firefly.id), curses.A_REVERSE)
            #     else:
            #         screen.addstr(y, x, str(firefly.id))

            # phase display version
            for f, firefly in enumerate(fireflies):
                x = firefly.id * 2
                y = height - int(firefly.phase * (height - 1)) - 1
                if firefly.recovery > 0:
                    screen.addstr(y, x, "X")
                else:
                    screen.addstr(y, x, " ", curses.A_REVERSE)                               
        except Exception as e:
            log.error(e)

        screen.refresh()
        time.sleep(FRAMERATE)


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
        self.t_previous = time.time()
        self.start()

    def run(self):
        while True:
            t = time.time()
            t_elapsed = t - self.t_previous
            self.phase = min(self.phase + (t_elapsed * self.frequency), 1.0)
            self.capacitor = self.f(self.phase)
            if self.recovery > 0:
                self.recovery -= t_elapsed
            if self.capacitor >= 1.0:
                self.fire()             
            self.t_previous = t
            time.sleep(0.001)

    def bump(self):
        if self.recovery <= 0 and self.capacitor < 1.0:
            log.info(f"--> {self.id} got bumped")
            self.capacitor = min(self.capacitor + BUMP, 1.0)
            self.phase = self.f_inv(self.capacitor)

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

    def __repr__(self):
        return f"{self.id}: {self.phase}"


wrapper(main)



'''

this is working well, and explicably, other than the weirdness in the lgos


ok, so next step -- what are our variables?

frequency first

'''