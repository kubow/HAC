

class Temp(object):
    def __init__(self, value, unit="C"):
        self.value = value
        self.unit = unit.upper()
        scales = {
                    'C': ('Celsius degrees ', 1, 0),
                    'F': ('Farenheit degrees ', 1.8, 32),
                    'K': ('Kelvin', 1, 273.15)
                }
        
    def to_c(self):
        if self.unit == "K":
            return self.value - 273.15
        elif self.unit == "F":
            return (self.value - 32) * 9 / 5
        else:
            return self.value
    
    def to_k(self):
        if self.unit == "C":
            return self.value + 273.15
        elif self.unit == "F":
            return 5/9*(self.value - 32) + 273.15
        else:
            return self.value

    def to_f(self):
        if self.unit == "C":
            return 9/5*(self.value) + 32
        if self.unit == "K":
            return 9/5*(self.value - 273.15) + 32
