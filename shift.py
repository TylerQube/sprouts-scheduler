class Shift:
    def __init__(self, initiative, day, time, capacity):
        self.initiative = initiative
        self.day = day
        self.time = time
        self.capacity = capacity
        self.volunteers = []
        self.num_available = 0

    def __str__(self):
        return f"Initiative: {self.initiative}\nDay: {self.day}\nTime: {self.time}\nCapacity: {len(self.volunteers)} / {self.capacity}\nNum Available: {self.num_available}"

    def add_volunteer(self, name):
        if len(self.volunteers) >= self.capacity:
            return False
        if name in self.volunteers:
            return False
        self.volunteers.append(name)
        return True

    def remove_volunteer(self, name):
        if name in self.volunteers:
            self.volunteers.remove(name)

    def __repr__(self):
            return "Shift(%s, %s, %s)" % (self.initiative, self.day, self.time)
    def __eq__(self, other):
        if not isinstance(other, Shift):
            return False
        return ((self.initiative == other.initiative) 
                and (self.day == other.day) 
                and (self.time == self.time))
    def __ne__(self, other):
        return (not self.__eq__(other))
    def __hash__(self):
        return hash(self.__repr__())