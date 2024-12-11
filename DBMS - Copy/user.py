from database import get_connection
import mysql.connector

class User:
    @staticmethod
    def add_user(first_name, last_name, email, phone, password, role):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
            INSERT INTO Users (first_name, last_name, email, phone, password, role)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (first_name, last_name, email, phone, password, role))
            connection.commit()
            print("User added successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            connection.close()

    @staticmethod
    def list_users():
        connection = get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM Users")
            users = cursor.fetchall()
            return users
        except mysql.connector.Error as err:
            print(f"Error fetching users: {err}")
            return []
        finally:
            connection.close()

    @staticmethod
    def delete_user(user_id):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM Users WHERE user_id = %s", (user_id,))
        connection.commit()
        print("User deleted successfully!")
        connection.close()
