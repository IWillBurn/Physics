class Engine:
    def __init__(self, environment):
        self.entities = []
        self.environment = environment

    def step(self):
        for entity in self.entities:
            entity.step()
