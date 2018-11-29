import pyodbc
import csv

#  connect to database
connection_string = 'Driver={ODBC Driver 17 for SQl server};Server=DESKTOP-1U0PR0M\SQLEXPRESS;Database=Avocado;Trusted_Connection=yes;'
conn =  pyodbc.connect(connection_string,autocommit=True)
curs = conn.cursor()

#  create table
curs.execute(
    '''
    create table avocado_data(
     Weird_Number float 
    ,Sell_Date date
    ,Average_price float
    ,Total_Volume float
    ,Small float
    ,Large float
    ,Xlarge float
    ,Total_Bags float
    ,Small_Bags float
    ,Large_Bags float
    ,XLarge_Bags float
    ,Type_of_Sell char(30)
    ,Year_of_Sell date
    ,Region char(30)
    )
    '''
    )

#  insert data
insert_query = 'insert into avocado_data (Weird_Number, Sell_Date, Average_price, Total_Volume, Small, Large, Xlarge, Total_Bags, Small_Bags, Large_Bags, XLarge_Bags, Type_of_Sell, Year_of_Sell, Region) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
with open(r'C:/Users/cdevi/Desktop/MIS 5400 Desktop/Project/avocado.csv', 'r',encoding='utf8') as cpi_file:
    cpi = csv.reader(cpi_file)
    curs.executemany(insert_query, cpi)




