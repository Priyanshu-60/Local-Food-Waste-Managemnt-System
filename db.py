import mysql.connector


# DB Connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="harshita@91199",
        database="food_donations"
    )