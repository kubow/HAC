''' Commands to deal with mathematic operations,
both algebra and geometry,
use alone to run simple calculator '''

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
