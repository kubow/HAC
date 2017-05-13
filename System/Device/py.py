import serial

ser = serial.Serial('/dev/ttyS0', 9200, timeout=0)
while 1:
    recieved = ser.readline().replace('\r\n', ' ')
    print(recieved)  
