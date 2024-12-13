import mysql.connector
from mysql.connector import errorcode

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "1234"

def setup_database():
    try:
        conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
        cursor = conn.cursor()

        # Database and user setup
        cursor.execute("DROP DATABASE IF EXISTS saramin_db;")
        cursor.execute("CREATE DATABASE saramin_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;")

        cursor.execute("DROP USER IF EXISTS 'flask_user'@'localhost';")
        cursor.execute("DROP USER IF EXISTS 'flask_user'@'%';")
        cursor.execute("CREATE USER 'flask_user'@'localhost' IDENTIFIED BY '555555';")
        cursor.execute("GRANT ALL PRIVILEGES ON saramin_db.* TO 'flask_user'@'localhost';")
        cursor.execute("CREATE USER 'flask_user'@'%' IDENTIFIED BY '555555';")
        cursor.execute("GRANT ALL PRIVILEGES ON saramin_db.* TO 'flask_user'@'%';")
        cursor.execute("FLUSH PRIVILEGES;")

        print("Database and user setup completed successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def setup_tables():
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database="saramin_db"
        )
        cursor = conn.cursor()

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL UNIQUE,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Create saramin_jobs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS saramin_jobs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                company VARCHAR(255) NOT NULL,
                location VARCHAR(255) NOT NULL,
                salary VARCHAR(255),
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Create favorites table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                job_id INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (job_id) REFERENCES saramin_jobs(id) ON DELETE CASCADE
            );
        """)

        print("Tables created successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    setup_database()
    setup_tables()
