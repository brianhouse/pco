import threading
import math
import time
from util import *
from util import midi

# percent of phase
BUMP = 1/100
RECOVERY = 20/100

nodes = []


class Node(threading.Thread):

    last_id = 0

    def __init__(self, x, y, phase, frequency, note):
        threading.Thread.__init__(self, daemon=True)
        self.id = Node.last_id
        Node.last_id += 1
        nodes.append(self)
        self.x = x
        self.y = y
        self.frequency = frequency
        self.phase = phase
        self.capacitor = self.f(self.phase)
        self.recovery = 0.0
        self.t_previous = time.time()
        self.listeners = []
        self.note = note

    def listen(self, node):
        if node is self:
            return
        self.listeners.append(node)

    def run(self):
        while True:
            try:
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
            except Exception as e:
                log.error(log.exc(e))

    def bump(self):
        if self.recovery <= 0 and self.capacitor < 1.0:
            log.info(f"--> {self.id} got bumped")
            self.capacitor = min(self.capacitor + BUMP, 1.0)
            self.phase = self.f_inv(self.capacitor)

    def fire(self):
        log.info(f"FIRE {self.id}")
        midi.out.send_note(5, self.note, 0)
        midi.out.send_note(5, self.note, 127)
        self.phase = 0.0
        self.capacitor = 0.0
        self.recovery = RECOVERY
        for node in self.listeners:
            node.bump()

    def f(self, x): # x is the phase
        return math.sin((math.pi / 2) * x)

    def f_inv(self, y): # y is the phase
        return (2 / math.pi) * math.asin(y)

    def __repr__(self):
        return f"{self.id}: {self.phase}"
