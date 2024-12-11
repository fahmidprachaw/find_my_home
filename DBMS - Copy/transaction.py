from database import get_connection
from datetime import datetime
import mysql.connector

class Transaction:
    @staticmethod
    def add_transaction(user_id, house_id, amount):
        connection = get_connection()
        cursor = connection.cursor()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
        INSERT INTO Transactions (user_id, house_id, amount, date)
        VALUES (%s, %s, %s, %s)
        """, (user_id, house_id, amount, date))
        connection.commit()

        # Mark the house as booked
        cursor.execute("UPDATE Houses SET status = 'booked' WHERE house_id = %s", (house_id,))
        connection.commit()

        print("Transaction added successfully!")
        connection.close()

    @staticmethod
    def list_transactions_by_owner(owner_id):
        connection = get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("""
            SELECT t.transaction_id, t.user_id, u.first_name, u.last_name, t.amount, t.date
            FROM Transactions t
            INNER JOIN Users u ON t.user_id = u.user_id
            INNER JOIN Houses h ON t.house_id = h.house_id
            WHERE h.owner_id = %s
            """, (owner_id,))
            transactions = cursor.fetchall()
            return transactions
        except mysql.connector.Error as err:
            print(f"Error fetching transactions: {err}")
            return []
        finally:
            connection.close()
