#!venv/bin/python

import curses
import random
import time
from curses import wrapper
from util import *
from node import *
from util.plotter import *

log.info("////////////////////////////////")

def wind(x):
    return math.sin(math.pi * (x - .5)) * .5 + .5
    # .5s are horiz shift, squish, and translate up, respectively

def wind2(x):
    return math.sin(math.pi * (x - .5)) + .5

def f(x): # x is the phase
    return math.sin((math.pi / 2) * x)

def f_inv(y): # y is the phase
    return (2 / math.pi) * math.asin(y)


def f3(x):
    y = math.sin((math.pi / 2) * x * 2) * .5
    if x > .5:
        y *= -1
        y += 1
    return y

def f3_inv(x):
    x *= -1
    x += 1
    y = math.sin((math.pi / 2) * x * 2) * .5
    if x < .5:
        y *= -1
        y += 1
    y *= -1
    y += 1
    return y

plot(wind, color="red")
plot(wind2, color="blue")
# plot(f_inv, color="red")
# plot(f3, color="orange")
# plot(f3_inv, color="white")
# plot(f_inv)
show_plots()


SPATIAL = True
PHASE = False
FRAMERATE = 1/60

# # 8 random nodes, all connected
# for x in range(8):
#     Node(random.random(), random.random(), random.random(), 1, 60 + x)
# for node in nodes:
#     Node.listeners.extend(nodes)


# what should the fs be?
covert_pulse = Node(10/100, 20/100, 0, 1, 36)
covert_counter = Node(20/100, 20/100, 0, 3, 50)

covert_counter.listen(covert_pulse)
covert_pulse.listen(covert_counter)

onset = Node(30/100, 20/100, 0, 2, 40)
# onset.listen(covert_pulse)
onset.listen(covert_counter)

covert_pulse.listen(onset)


def main(screen):
    for node in nodes:
        node.start()
    height, width = screen.getmaxyx()
    curses.curs_set(0)
    while True:
        screen.clear()
        try:
            if SPATIAL:
                # spatial version
                for f, node in enumerate(nodes):
                    x, y = int(node.x * width), int(node.y * height)
                    if node.phase < 0.1:
                        screen.addstr(y, x, str(node.id), curses.A_REVERSE)
                    else:
                        screen.addstr(y, x, str(node.id))
            if PHASE:
                # phase display version
                for f, node in enumerate(nodes):
                    x = node.id * 2
                    y = height - int(node.phase * (height - 1)) - 2
                    if node.recovery > 0:
                        screen.addstr(y, x, "X")
                    else:
                        screen.addstr(y, x, " ", curses.A_REVERSE)
        except Exception as e:
            log.error(log.exc(e))

        screen.refresh()
        time.sleep(FRAMERATE)



wrapper(main)
