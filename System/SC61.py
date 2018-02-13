''' Commands to deal with mathematic operations,
both algebra and geometry,
use alone to run simple calculator '''
import sys #for pygt graph
import decimal
from random import randint, random, uniform

try:
    import numpy
    num_wrap = True
except ImportError:
    print('numpy not installed, trying to improvise ...')
    num_wrap = False

try:
    import pyqtgraph as pg
    plotting = True
except ImportError:    
    print('QT graphing not installed, must plot on command line')
    plotting = False


class Number(object):
    def __init__(self, value=0):
        self.val = value
        
    def generate_random(low=0, high=100, integer=False):
        if integer:
            return randint(int(low), int(high))
        else:
            return uniform(low, high)
        
    def generate_random_series(series_size=1000):
        numpy.random.normal(size=series_size)


class Matematize(object):
    def __init__(self, value, definition=10):
        self.val = value
        self.dec_val = decimal.Decimal(value)
        self.is_num = value.isdigit()
        self.precise = len(str(n))-1 
        self.scale = len(str(n).split('.')[1])
        self.in_def = definition
        if self.dec_val >= 0:
            self.is_neg = False
        else:
            self.is_neg = True
        if self.dec_val < 1:
            self.percentage = str(self.dec_val * 100) + '%'
        else:
            self.percentage = str(self.dec_val / 100) + '%'


# Math functions
class Operations:
    '''Basic numeric operations
    define precissness'''
    x = y = 0.00
    
    def add(x, y):
       """This function adds two numbers"""
       return x + y

    def sbt(x, y):
       """This function subtracts two numbers"""
       return x - y

    def mlt(x, y):
       """This function multiplies two numbers"""
       return x * y

    def div(x, y):
       """This function divides two numbers"""
       if y == 0 or y is not None:
        return x / y
       else:
        return None
        
    def pwr(x, y):
        """Returns y power of a number"""
        return x ** y
        
    def fact(x):
        """ Return factorial of a number"""
        if x < 0:
            return None
        elif x > 0:
            return x * (x-1)
        else:
            return 1            
                
def graphing():
    n = Number()
    plot_data = n.generate_random_series(series_size=1000)
    image_data = n.generate_random_series(series_size=size=(500,500))

    pg.plot(plot_data, title="Simplest possible plotting example")
    pg.image(data, title="Simplest possible image example")

    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()

    # Switch to using white background and black foreground
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')

if __name__ == '__main__':
    """Interactive part for standalone running"""
    print("Select operation.")
    print("1.Add")
    print("2.Subtract")
    print("3.Multiply")
    print("4.Divide")

    choice = input("Enter choice(1/2/3/4):")
    num1 = int(input("Enter first number: "))
    num2 = int(input("Enter second number: "))

    op = Operations()

    if choice == '1':
       print(num1,"+",num2,"=", op.add(num1,num2))

    elif choice == '2':
       print(num1,"-",num2,"=", op.sbt(num1,num2))

    elif choice == '3':
       print(num1,"*",num2,"=", op.mlt(num1,num2))

    elif choice == '4':
       print(num1,"/",num2,"=", op.div(num1,num2))
    else:
       print("Invalid input")
