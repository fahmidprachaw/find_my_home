import mysql.connector

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="prachaw1234",  # Replace with your MySQL password
            database="find_Home"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        phone VARCHAR(15),
        password VARCHAR(100) NOT NULL,
        role ENUM('admin', 'customer', 'flat_owner') NOT NULL
    );
    """)

    # Houses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Houses (
        house_id INT AUTO_INCREMENT PRIMARY KEY,
        type_name VARCHAR(50) NOT NULL,
        description TEXT,
        location VARCHAR(100) NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        owner_id INT NOT NULL,
        status ENUM('available', 'booked') DEFAULT 'available',
        approved BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (owner_id) REFERENCES Users(user_id)
    );
    """)

    # Transactions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Transactions (
        transaction_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        house_id INT NOT NULL,
        amount DECIMAL(10, 2) NOT NULL,
        date DATETIME NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users(user_id),
        FOREIGN KEY (house_id) REFERENCES Houses(house_id)
    );
    """)

    # Add default admin user
    cursor.execute("""
    INSERT IGNORE INTO Users (first_name, last_name, email, phone, password, role)
    VALUES ('Admin', 'User', 'admin@gmail.com', '1234567890', 'admin123', 'admin')
    """)

    connection.commit()
    connection.close()
