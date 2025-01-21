class Phase:
    def __init__(self, name, exists, terminated, start_time, end_time, errors):
        self.name = name
        self.exists = exists
        self.terminated = terminated
        self.start_time = start_time
        self.end_time = end_time
        self.errors = errors

    def to_dict(self):
        return {
            'name': self.name,
            'exists': self.exists,
            'terminated': self.terminated,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'errors': self.errors
        }
