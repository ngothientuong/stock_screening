import pyodbc

# Loop through all the drivers we have access to
for driver in pyodbc.drivers():
    print(driver)
# define the server name and the database name
server = 'TuongDesktop\TUONGSQL'
database = 'tradingdb'
db_username = 'XXXXXXX'
db_password = 'XXXXXXX'

#price_data = [[1, 2.00, 3.00, 1.00, 2.40, 100.00, '1/2/2019'],
#              [2, 3.00, 3.00, 5.00, 9.00, 300.00, '2/5/2020'],
#              [3, 4.00, 2.00, 1.00, 2.40, 200.00, '3/7/2021']]

price_data = [[2.00, 3.00, 1.00, 2.40, 100.00, '1/2/2019'],
              [3.00, 3.00, 5.00, 9.00, 300.00, '2/5/2020'],
              [4.00, 2.00, 1.00, 2.40, 200.00, '3/7/2021']]

# define our connection string
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                       SERVER=' + server + '; \
                       DATABASE=' + database + '; \
                       UID=' + db_username + '; \
                       PWD=' + db_password)
                       #Trusted Connection=yes;')

# create the connection cursor
cursor = cnxn.cursor()

# define our insert query
insert_query = '''INSERT INTO stocktb(close_price, high, low, open_price, volume, day_value)
                  VALUES (?, ?, ?, ?, ?, ? );'''

# loop through each row in the matrix
for row in price_data:
    # define the value to insert
    values = (row[0], row[1], row[2], row[3], row[4], row[5])
    
    # insert the data into the database
    cursor.execute(insert_query, values)
# commit the inserts
cnxn.commit()

# grab all the rows in our database table
cursor.execute('SELECT * FROM stocktb')

# loop through the results
for row in cursor:
    print(row)
    
cursor.close()
cnxn.close()

# del cursor, cnxn, insert_query, db_password, db_username, database, server;