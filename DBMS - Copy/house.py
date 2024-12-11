from database import get_connection
import mysql.connector

class House:
    @staticmethod
    def add_house(owner_id, type_name, description, location, price):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO Houses (type_name, description, location, price, owner_id)
        VALUES (%s, %s, %s, %s, %s)
        """, (type_name, description, location, price, owner_id))
        connection.commit()
        print("House added successfully!")
        connection.close()

    @staticmethod
    def list_houses(status='available', approved=True):
        connection = get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("""
            SELECT * FROM Houses WHERE status = %s AND approved = %s
            """, (status, approved))
            houses = cursor.fetchall()
            return houses
        except mysql.connector.Error as err:
            print(f"Error fetching houses: {err}")
            return []
        finally:
            connection.close()

    @staticmethod
    def update_house_status(house_id, status):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("UPDATE Houses SET status = %s WHERE house_id = %s", (status, house_id))
        connection.commit()
        print("House status updated!")
        connection.close()

    @staticmethod
    def list_owner_houses(owner_id):
        connection = get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM Houses WHERE owner_id = %s", (owner_id,))
            houses = cursor.fetchall()
            return houses
        except mysql.connector.Error as err:
            print(f"Error fetching owner houses: {err}")
            return []
        finally:
            connection.close()
