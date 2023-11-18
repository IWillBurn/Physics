
class Environment:
    def __init__(self, params):
        self.params = params
        self.sdt = params["step_delta_time"]

    def set(self, key, value):
        self.params[key] = float(value)

    def on_ground(self, position):
        return (self.params["ground"][0] * position.x + self.params["ground"][1] * (self.params["screen_height"] / 2 - position.y)) > 0
