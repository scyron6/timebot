class Client:
    def __init__(self, minutes):
        self.total_minutes = minutes
        self.minutes_per_work = {}

    def add_minutes(self, minutes):
        self.total_minutes += minutes
    
    def add_minutes_to_work(self, work, minutes):
        if isinstance(work, float):
            work = 'Unlabeled Work'
        if work in self.minutes_per_work:
            self.minutes_per_work[work] += minutes
        else:
            self.minutes_per_work[work] = minutes