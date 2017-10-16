import pysimpledmx
from threading import Timer
from fixtures import RGBFixture, RGBWFixture
from states import STATE_LIST

PATCH = [
    (1, 1, RGBWFixture),
    (2, 5, RGBFixture),
    (3, 8, RGBWFixture),
    (4, 12, RGBFixture),
    (5, 15, RGBWFixture),
    (6, 19, RGBFixture),
    (7, 22, RGBWFixture),
    (8, 26, RGBFixture),
]


class Manager():
    fixtures = {}
    transition_count = 0
    timer = None

    def __init__(self):
        self.device = pysimpledmx.DMXConnection("/dev/ttyUSB0")
        for fixture in PATCH:
            self.fixtures[fixture[0]] = fixture[2](self, fixture[1])

    def set_state(self, state):
        if state in STATE_LIST:
            s = STATE_LIST[state]
            for fixture in self.fixtures:
                if fixture in s:
                    self.fixtures[fixture].set_level(s[fixture]["level"])
                    self.fixtures[fixture].set_color(s[fixture]["color"])
                else:
                    self.fixtures[fixture].set_level(s["level"])
                    self.fixtures[fixture].set_color(s["color"])
        else:
            for fixture in self.fixtures:
                self.fixtures[fixture].set_level(0)

    def change(self):
        for fixture in self.fixtures:
            self.fixtures[fixture].push_values()
        self.render()

    def transition(self):
        if self.transition_count:
            self.transition_finish()
        # default transition in 20 steps in 1 second
        self.transition_count = 19
        for fixture in self.fixtures:
            self.fixtures[fixture].transition_start()
        self.transition_step()

    def transition_step(self):
        for fixture in self.fixtures:
            self.fixtures[fixture].transition_step()
            self.fixtures[fixture].push_values()

        self.transition_count = self.transition_count - 1

        if self.transition_count:
            self.render()
            self.timer = Timer(0.05, self.transition_step)
            self.timer.start()
        else:
            self.transition_finish()

    def transition_finish(self):
        try:
            self.timer.cancel()
            self.timer = None
        except Exception:
            self.timer = None
        for fixture in self.fixtures:
            self.fixtures[fixture].transition_finish()
        self.render()

    def render(self):
        self.device.render()

