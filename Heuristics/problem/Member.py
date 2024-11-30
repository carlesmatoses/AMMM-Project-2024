class Member(object):
    def __init__(self, ID:int, departmentID:int, compatibility:list[float]):
        self.departmentID = departmentID
        self.memberId = ID
        self.compatibility = compatibility
        self.gene = 1
        
        # ranking calculation
        self.weight = 0
        for i in self.compatibility:
            if i > 0.15:
                self.weight += i
            elif 0 < i <= 0.15:
                self.weight += 0.05
        self.weight = self.weight / len(self.compatibility)
        
    def getId(self):
        return self.memberId
    
    def getDepartmentID(self):
        return self.departmentID
    
    def getCompatibility(self, member:int) -> bool:
        if self.compatibility[member] == 0.0:
            return False
        return True
    
    def getCompatibilityValue(self, member:int) -> float:
        return self.compatibility[member]

    def getWeight(self):
        return self.weight
    
    def logCompatibility(self):
        print(f"Member {self.memberId} is compatible with: {self.compatibility}")

    def __str__(self):
        return f"Member: {self.memberId}, group: {self.departmentID}"
