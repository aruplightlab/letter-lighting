class Fixture():
    initial_params = {
        0: {
            'name': 'dimmer',
            'value': 0,
        },
    }

    def __init__(self, uid, manager, start_addr):
        self.uid = uid
        self.start_addr = start_addr
        self.manager = manager
        self.virtual_dimmer = 1
        self.changed = True
        self.params = self.initial_params.copy()

    def push_values(self):
        print(self.uid, self.params)
        if self.changed:
            for param in self.params:
                if "value_next" in self.params[param]:
                    value = self.params[param]["value_next"]
                    self.params[param]["value"] = value
                else:
                    value = self.params[param]["value"]
                chan = self.start_addr + param + 1
                self.changed = False
                if self.manager.device:
                    self.manager.device.setChannel(int(chan), int(value))
                else:
                    # print(int(chan), int(value))
                    pass

    def transition_start(self):
        for param in self.params:
            p = self.params[param]
            if "value_next" in p:
                p["value_final"] = p["value_next"]
            else:
                p["value_final"] = p["value"]

    def transition_step(self):
        steps_left = self.manager.transition_count
        for param in self.params:
            p = self.params[param]
            difference = p["value_final"] - p["value"]
            if difference:
                self.changed = True
                step = int(difference / steps_left)
                if step:
                    p["value_next"] = p["value"] + step
        self.push_values()

    def transition_finish(self):
        for param in self.params:
            value = self.params[param].pop("value_final", None)
            if value:
                self.params[param]["value"] = value
            self.params[param].pop("value_next", None)
        self.changed = False

    def set_color(self, color):
        pass

    def set_level(self, level):
        self.virtual_dimmer = float(level) / 255
        # print(self.uid, "level", self.params)
        self.adjust_level()
        # print(self.uid, "level adjust", self.params)

    def adjust_level(self):
        for param in self.params:
            if "value_nondim" not in self.params[param]:
                self.params[param]["value_nondim"] = (
                    self.params[param]["value"])
            self.params[param]["value_next"] = int(
                self.params[param]["value_nondim"] * self.virtual_dimmer)
        self.changed = True


class RGBFixture(Fixture):
    initial_params = {
        0: {
            'name': 'red',
            'value': 0,
        },
        1: {
            'name': 'green',
            'value': 0,
        },
        2: {
            'name': 'blue',
            'value': 0,
        },
    }

    def set_color(self, color):
        # print(self.uid, "color", color)
        color = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
        for param in self.params:
            self.params[param]["value_nondim"] = color[param]
        # print(self.uid, "color", self.params)
        self.adjust_level()
        # print(self.uid, "color adjust", self.params)


class RGBWFixture(Fixture):
    initial_params = {
        0: {
            'name': 'red',
            'value': 0,
        },
        1: {
            'name': 'green',
            'value': 0,
        },
        2: {
            'name': 'blue',
            'value': 0,
        },
        3: {
            'name': 'white',
            'value': 0,
        },
    }

    def set_color(self, color):
        color = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
        color = color + (min(color), )
        for param in self.params:
            self.params[param]["value_nondim"] = color[param]
        self.adjust_level()
