import psycopg2
 
conn = psycopg2.connect(dbname="postgres", user="begimai", password="1", host="localhost")
cursor = conn.cursor()
 
conn.autocommit = True
# команда для создания базы данных metanit
sql = "CREATE DATABASE task11"
 
# выполняем код sql
cursor.execute(sql)
print("База данных успешно создана")
 
cursor.close()
conn.close()

# строка подключения
class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://begimai:1@localhost/task11"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

DATABASE_URL = "postgresql://begimai:1@localhost/task11"
