from phase import Phase

class Chain:
    def __init__(self, name, terminated, start_time, end_time, phases):
        self.name = name
        self.terminated = terminated
        self.start_time = start_time
        self.end_time = end_time
        self.phases = phases
        

    def to_dict(self):
        return {
            'name': self.name,
            'terminated': self.terminated,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'phases': [phase.to_dict() for phase in self.phases]
        }