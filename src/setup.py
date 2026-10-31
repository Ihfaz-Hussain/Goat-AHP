import os 
import psycopg2 
from dotenv import load_dotenv

load_dotenv()

#get database cofiguration from environment variables
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

#Establish a connection to the database
try:
    connection = psycopg2.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        dbname=db_name
    )
    print("Database connection established successfully.")

    with connection.cursor() as cursor:
        cursor.execute("SELECT current_database();")
        result = cursor.fetchone()
        print(f"Connected to database: {result[0]}")
except psycopg2.Error as e:
    print(f"Error connecting to the database: {e}")
finally:
    if connection is not None:
        connection.close()
        print("Database connection closed.")
