'''

    Author:       Kevin Netherton
    Purpose:      Provides some utility functions for excel.  Motivation
                  was to provide a means of calculating the excel
                  alphabetic column name (A, B, C, AB, AC, etc...) from
                  a numeric value.  Example 0 = A, 1=b so on...
                  
                  also includes functionality to parse excel cell addresses
                  example take AA34:DC:21 and return as a list:
                  ('AA', 34, 'DC', 21)
                  use the parseRangeString function for this, or the 
                  parseCellLocationString to parse a single cell address
                  like A3 into A and 3.
                  
                  
    Date:         11-01-2008
    Arguments:    Depends!
    Outputs:      
    Dependencies:
    
    Usage Example:
        This script/module as purpose statement above states provides
        functionality to translate a numeric column into the alphabetic 
        columns which excel uses.
        
        To use:
        A) ensure the path to this folder is included in your 
           pythonpath environment variable.
        B) look at the code example below showing how it can 
           be used
        ----------------------------------------------------
        # import the module
        import xl_Funcs
        
        # create an xlFunc object
        xlFuncObj = xl_Funcs.xlFuncs()
        
        # do the number translation, in the example
        # below we are translating the number 3
        # if we excute this code and print
        # xlColLetter it will be equal to C
        xlColLetter = xlFuncObj.num2String(3)
        
        # thats it.
    
                 
    History:     
    --------------------------------------------------------------
    Date:
    Author:
    Modification:
    --------------------------------------------------------------
   
'''
import re

class xlFuncs:
    '''
    A class which contains functionality to translate between 
    numeric values and excel column values.  Assumes that 
    column 1 is the starting column, ie column 1 should
    translate to A
    '''
    
    
    
    def __init__(self):
        self.letters = 'abcdefghijklmnopqrstuvwxyz'
    
    def num2String(self, origNum):
        ''' 
        Takes a column number and converts it to a string
        representation of that number.
        example 1 = a
                2 = b
                3 = c
                26 = z
                27 = aa
                28 = ab
                etc.
                
        '''
        num = origNum - 1
        if origNum <= 0:
            raise 'InvalidNumber', 'Need to provide a number greater than 0'
        # the conversion is essentially a conversion to a base 26 number
        # system.  In a base 26 number system the first number has to be
        # 0.  This allows representation of numbers like 10 in base 26.
        # Because excel starts with a being column 1 the assumption is that
        # column 1 represents column a.  For this reason we subtract 1 from the 
        # submitted number for the conversion.
        
        base26Number = self.tobase26(num)
        outString = ''
        list = base26Number.split('|')
        firstNum = True
        if len(list) == 1:
            firstNum = False
        for i in list:
            if i == '':
                break
            elif firstNum:
                firstNum = False
                i = int(i) - 1
            outString = outString + self.letters[int(i)]
        #print origNum, num, base26Number, outString
        return outString
    
    def tobase26(self, n,result=''):
        '''
        Converts a given number from base 10 to base 26.
        
        The format for base 26 numbers will be like:
        1|24|3
        Where the | symbol is used to delimit columns.
        '''
        b = 26
        if n == 0:
            if result:
                return result
            else:
                return '0'
        else:
            num1 = ((n)/b) 
            if result:
                string1 = str((n)%b) + '|' + result
            else:
                string1 = str((n)%b)
            return self.tobase26(num1, string1)
        
    def test(self):
        '''
        From the name of the script this is a testing module which
        will test the num2String module with various numbers to ensure
        that the algorithm is working correctly.
        '''
        self.num2String(1)
        self.num2String(25)
        self.num2String(26)
        self.num2String(27)
        self.num2String(51)
        self.num2String(52)
        self.num2String(53)
        self.num2String(78)
        self.num2String(79)
        self.num2String(162)
        self.num2String(676)
        self.num2String(677)
        self.num2String(3458)
        self.num2String(3457)
        self.num2String(17576)
        self.num2String(17577)
        #print 'base26: 27:', self.tobase26(27)
        #print 'base26: 3458:', self.tobase26(3458)
        #print 'base26: 3458:', self.tobase26(3457)
    
    def parseCellLocationString(self, cellLocation):
        '''
        This method will recieve a cellLocation like:
        A1 or AE799 and return two values:
         1) alphabetic position / column string (A AE)
         2) numeric position / row number (1, 799)
        
        example input: A3
                output A, 3
        
                input AE799
                output AE, 799
        '''
        numbers = re.sub('\D', '', cellLocation)
        letters = re.sub('\d', '', cellLocation)
        return letters, numbers
    
    def parseRangeString(self, rangeString):
        '''
        Recieves a ranges string like A1:M33
        and returns 4 values.
        
        1) start column (A)
        2) start row    (1)
        3) end column   (M)
        4) end row      (33)
        '''
        list = rangeString.split(':')
        startCell = list[0]
        endCell = list[1]
        startLetter, startNumber = self.parseCellLocationString(startCell)
        endLetter, endNumber = self.parseCellLocationString(endCell)
        return startLetter, startNumber, endLetter, endNumber
        
if __name__ == '__main__':
    obj =  xlFuncs()
    obj.test()
    
    
    
        
        