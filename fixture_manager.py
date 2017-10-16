import pysimpledmx
from threading import Timer
from fixtures import RGBFixture, RGBWFixture

PATCH = [
    (1, 1, RGBWFixture),
    # (2, 5, RGBFixture),
    # (3, 8, RGBWFixture),
    # (4, 12, RGBFixture),
    # (5, 15, RGBWFixture),
    # (6, 19, RGBFixture),
    # (7, 22, RGBWFixture),
    # (8, 26, RGBFixture),
]


class Manager():
    fixtures = {}
    transition_count = 0
    timer = None

    def __init__(self):
        # self.device = pysimpledmx.DMXConnection("/dev/ttyUSB0")
        for fixture in PATCH:
            self.fixtures[fixture[0]] = fixture[2](self, fixture[1])

    def set_state(self, state):
        if state:
            for fixture in self.fixtures:
                self.fixtures[fixture].set_level(255)
                self.fixtures[fixture].set_color("FF0000")
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
        # default transition in 10 steps / 1 second
        self.transition_count = 9
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
            self.timer = Timer(0.1, self.transition_step)
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
        # self.device.render()
        print("rendered")
