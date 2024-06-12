class Shift:
    def __init__(self, initiative, day, time, capacity):
        self.initiative = initiative
        self.day = day
        self.time = time
        self.capacity = capacity
        self.volunteers = []
    
    def __str__(self):
        return f"Initiative: {self.initiative}\nDay: {self.day}\nTime: {self.time}\nCapacity: {self.capacity}"
        
    def add_volunteer(self, name):
        self.volunteers.append(name)