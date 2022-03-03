class Employee:
    def __init__(self):
        self.minutes_per_client = {}
        self.minutes_per_task = {}
        self.minutes_per_role = {}
        self.work_per_client = {}

    def add_hours_to_client(self, client, minutes):
        if client in self.minutes_per_client:
            self.minutes_per_client[client] += minutes
        else:
            self.minutes_per_client[client] = minutes
    
    def add_hours_to_task(self, task, minutes):
        if task in self.minutes_per_task:
            self.minutes_per_task[task] += minutes
        else:
            self.minutes_per_task[task] = minutes


    def add_hours_to_role(self, role, minutes):
        if role in self.minutes_per_role:
            self.minutes_per_role[role] += minutes
        else:
            self.minutes_per_role[role] = minutes
    
    def add_work_to_client(self, client, work, minutes):
        if isinstance(work, float):
            work = 'Unlabeled Work'
        if client in self.work_per_client:
            if work in self.work_per_client[client]:
                self.work_per_client[client][work] += minutes
            else:
                self.work_per_client[client][work] = minutes
        else:
            self.work_per_client[client] = {}
            self.work_per_client[client][work] = minutes