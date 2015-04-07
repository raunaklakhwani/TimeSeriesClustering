class DeviceInfo:
    def __init__(self, x, y, macaddress, firstlocatedtime, lastlocatedtime,index, block, blockNumber):
        self.x = x
        self.y = y
        self.macaddress = macaddress
        self.firstlocatedtime = firstlocatedtime
        self.lastlocatedtime = lastlocatedtime
        self.index = index
        self.block = block
        self.blockNumber = blockNumber
        
    def __eq__(self,other):
        return self.x == other.x and self.y == other.y and self.lastlocatedtime == other.lastlocatedtime and self.firstlocatedtime == other.firstlocatedtime
    
    def __str__(self):
        return str(self.index) + " " + str(self.block) + " (" + str(self.x) + ", " + str(self.y) + ") " + str(self.lastlocatedtime) + " " + str(self.firstlocatedtime) + " " + self.macaddress
