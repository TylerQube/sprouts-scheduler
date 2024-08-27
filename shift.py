class Shift:
    def __init__(self, initiative, day, time, capacity):
        self.initiative = initiative
        self.day = day
        self.time = time
        self.capacity = capacity
        self.volunteers = []
        self.num_available = 0

    def __str__(self):
        return f"Initiative: {self.initiative}\nDay: {self.day}\nTime: {self.time}\nCapacity: {len(self.volunteers)} / {self.capacity}"

    def add_volunteer(self, name):
        if len(self.volunteers) >= self.capacity:
            return False
        self.volunteers.append(name)
        return True

    def remove_volunteer(self, name):
        if name in self.volunteers:
            self.volunteers.remove(name)
