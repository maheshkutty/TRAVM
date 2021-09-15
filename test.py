import cx_Oracle
import os
import config


connection = cx_Oracle.connect(user = config.USER , password= config.PASSWORD, dsn= config.DSN, encoding="UTF-8")
cursor = connection.cursor()

# cursor.execute(" insert into train (TRAIN_NO , TRAIN_NAME , COST_PER_SEAT , SOURCE_STATE , SOURCE_DISTRICT , SOURCE_CITY , SOURCE_PINCODE , SOURCE_LINE , DESTN_STATE , DESTN_DISTRICT , DESTN_CITY , DESTN_PINCODE , DESTN_LINE , DEPARTURE_DATE , DEPARTURE_TIME , ARRIVAL_DATE , ARRIVAL_TIME , ADMIN_ID ) values('20110' , 'XSS Express' , 870 , 'Maha' , 'Mum' , 'Mum' , 400612 , '307/Apt.' , 'Odisha' , 'Ganjam' , 'Brahmapur' , 760011 , 'B Street' , '14-Mar-2021' , '10:00' , '16-Mar-2021' , '22:00' , 21 ) ")
# connection.commit()
# cursor.execute("SELECT * FROM UserDetails ")
# for row in cursor:
#     print(row)
print(connection.version)
cursor.close()
connection.close()