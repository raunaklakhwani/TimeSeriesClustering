class DeviceInfo:
    def __init__(self, x, y, macaddress, firstlocatedtime, lastlocatedtime):
        self.x = x
        self.y = y
        self.macaddress = macaddress
        self.firstlocatedtime = firstlocatedtime
        self.lastlocatedtime = lastlocatedtime
        
    def __eq__(self,other):
        return self.x == other.x and self.y == other.y and self.lastlocatedtime == other.lastlocatedtime and self.firstlocatedtime == other.firstlocatedtime
