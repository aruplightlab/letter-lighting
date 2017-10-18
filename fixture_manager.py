import pysimpledmx
from threading import Timer
from fixtures import RGBFixture, RGBWFixture
from states import STATE_LIST, STATE_LISTS

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

    def __init__(self, debug=False):
        if not debug:
            self.device = pysimpledmx.DMXConnection("/dev/ttyUSB0")
        else:
            self.device = None
        for fixture in PATCH:
            self.fixtures[str(fixture[0])] = fixture[2](
                fixture[0], self, fixture[1])

    def set_state(self, state):
        try:
            self.state_timer.cancel()
            self.state_timer = None
        except Exception:
            self.state_timer = None
        if state in STATE_LISTS:
            self.next_state(STATE_LISTS[state], 0)
        elif state in STATE_LIST:
            s = STATE_LIST[state]
            for fixture in self.fixtures:
                if str(fixture) in s:
                    self.fixtures[fixture].set_level(s[str(fixture)]["level"])
                    self.fixtures[fixture].set_color(s[str(fixture)]["color"])
                elif "level" in s and "color" in s:
                    self.fixtures[fixture].set_level(s["level"])
                    self.fixtures[fixture].set_color(s["color"])
        else:
            for fixture in self.fixtures:
                self.fixtures[fixture].set_color("000000")
                self.fixtures[fixture].set_level(0)

    def next_state(self, state_list, current, time=5):
        self.set_state(state_list[current])
        current = current + 1
        if current >= len(state_list):
            current = 0
        self.transition(time)
        self.state_timer = Timer(
            time, self.next_state, args=[state_list, current, time])
        self.state_timer.start()

    def change(self):
        for fixture in self.fixtures:
            self.fixtures[fixture].push_values()
        self.render()

    def transition(self, time=1):
        if self.transition_count:
            self.transition_finish()
        # default transition in 12 steps in 1 second
        self.transition_count = 15 * time
        for fixture in self.fixtures:
            self.fixtures[fixture].transition_start()
        self.transition_step()

    def transition_step(self):
        for fixture in self.fixtures:
            self.fixtures[fixture].transition_step()

        self.transition_count = self.transition_count - 1

        if self.transition_count:
            self.render()
            self.transition_timer = Timer(0.05, self.transition_step)
            self.transition_timer.start()
        else:
            self.transition_finish()

    def transition_finish(self):
        try:
            self.transition_timer.cancel()
            self.transition_timer = None
        except Exception:
            self.transition_timer = None
        for fixture in self.fixtures:
            self.fixtures[fixture].transition_finish()
        self.render()

    def render(self):
        if self.device:
            self.device.render()
        else:
            print("------ RENDERED")
