import sqlite3
# get tepmerature
# argument devicefile is the path of the sensor to be read,
# returns None on error, or the temperature as a float
def get_temp(devicefile):
    try:
        fileobj = open(devicefile,'r')
        lines = fileobj.readlines()
        fileobj.close()
    except:
        return None
    # get the status from the end of line 1 
    status = lines[0][-4:-1]
    # is the status is ok, get the temperature from line 2
    if status=="YES":
        print status
        tempstr= lines[1][-6:-1]
        tempvalue=float(tempstr)/1000
        print tempvalue
        return tempvalue
    else:
        print "There was an error."
        return None

# store the temperature in the database
def log_temperature(temp, dbname):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    curs.execute("INSERT INTO temps values(datetime('now'), (?))", (temp,))
    # commit the changes
    conn.commit()
    conn.close()
    
 temp_val = get_temp('xxx.db')