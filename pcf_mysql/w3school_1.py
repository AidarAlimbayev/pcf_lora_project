import mysql.connector
mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'pcf_user',
    passwd = '4568',
    database = 'pcf_database_1'
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE cows (id INT AUTO_INCREMENT PRIMARY KEY, cow_id VARCHAR(255), date_time VARCHAR(255), cow_weight VARCHAR(255), scales_model VARCHAR(255))")
