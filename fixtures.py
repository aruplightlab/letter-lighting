class Fixture():
    start_addr = 1
    params = {
        0: {
            'name': 'dimmer',
            'value': 255,
        },
    }

    def __init__(self, manager, start_addr):
        self.start_addr = start_addr
        self.manager = manager

    def push_values(self):
        for param in self.params:
            if "value_next" in self.params[param]:
                value = self.params[param]["value_next"]
                self.params[param]["value"] = value
            else:
                value = self.params[param]["value"]
            # self.manager.device.setChannel(
            #    self.start_addr + param,
            #    value)
        print("params set", self.start_addr, self.params)

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
                step = int(difference / steps_left)
                if step:
                    p["value_next"] = p["value"] + step

    def transition_finish(self):
        for param in self.params:
            value = self.params[param].pop("value_final", None)
            if value:
                self.params[param]["value"] = value
            self.params[param].pop("value_next", None)

    def set_level(self, level):
        pass

    def set_color(self, color):
        pass


class RGBFixture(Fixture):
    virtual_dimmer = 1
    params = {
        0: {
            'name': 'red',
            'value': 255,
        },
        1: {
            'name': 'green',
            'value': 255,
        },
        2: {
            'name': 'blue',
            'value': 255,
        },
    }

    def set_level(self, level):
        self.virtual_dimmer = (level / 255)
        for param in self.params:
            p = self.params[param]
            if "value_nondim" not in p:
                p["value_nondim"] = p["value"]
            p["value_next"] = int(p["value_nondim"] * self.virtual_dimmer)

    def set_color(self, color):
        color = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
        for param in self.params:
            self.params[param]["value_nondim"] = color[param]
        self.set_level()


class RGBWFixture(Fixture):
    virtual_dimmer = 1
    params = {
        0: {
            'name': 'red',
            'value': 255,
        },
        1: {
            'name': 'green',
            'value': 255,
        },
        2: {
            'name': 'blue',
            'value': 255,
        },
        3: {
            'name': 'white',
            'value': 255,
        },
    }

    def set_level(self, level):
        self.virtual_dimmer = (level / 255)
        self.adjust_level()

    def adjust_level(self):
        for param in self.params:
            p = self.params[param]
            if "value_nondim" not in p:
                p["value_nondim"] = p["value"]
            p["value_next"] = int(p["value_nondim"] * self.virtual_dimmer)

    def set_color(self, color):
        color = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
        color = color + (min(color), )
        for param in self.params:
            self.params[param]["value_nondim"] = color[param]
        self.adjust_level()