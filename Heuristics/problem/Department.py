class Department(object):
    def __init__(self, ID:int, capacity:int):
        self.ID = ID
        self.maxCapacity = capacity
        self.currentCapacity = capacity
        self.members = []

    def getId(self):
        return self.ID

    def getCurrentCapacity(self):
        return self.currentCapacity
    
    def assignMember(self, member:int):
        self.members.append(member)
        self.currentCapacity -= 1
        
    def unassignMember(self, member:int):
        self.members.remove(member)
        self.currentCapacity += 1

    def __str__(self):
        return f"Department: {self.ID}, capacity: {self.maxCapacity}"
