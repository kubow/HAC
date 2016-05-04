import MySQLdb

# connect to database
mydb = MySQLdb.connect("localhost","root","0dy5seuS","cars_db")

# define the function
def data_entry(cars_for_sale):

# cursor creation
    cursor = mydb.cursor()

#load the file 'cars_for_sale.txt' into the database under the table 'cars_for_sale'

    sql = """LOAD DATA LOCAL INFILE 'cars_for_sale.TXT'
        INTO TABLE cars_for_sale
        FIELDS TERMINATED BY '\t'
        LINES TERMINATED BY '\r\n'"""

    #execute the sql function above
    cursor.execute(sql)

    #commit to the database
    mydb.commit()

    #call data_entry(cars_for_sale) function
    data_entry(cars_for_sale)

mydb.close()

