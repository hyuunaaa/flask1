import mysql.connector
from mysql.connector import errorcode

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "1234"

def setup_database():
    try:
        conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
        cursor = conn.cursor()

        # 데이터베이스 삭제
        cursor.execute("DROP DATABASE IF EXISTS saramin_db;")
        # 데이터베이스가 없을 경우에만 생성
        cursor.execute("CREATE DATABASE IF NOT EXISTS saramin_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;")

        # 사용자 설정
        cursor.execute("CREATE USER IF NOT EXISTS 'flask_user'@'localhost' IDENTIFIED BY '555555';")
        cursor.execute("GRANT ALL PRIVILEGES ON saramin_db.* TO 'flask_user'@'localhost';")
        cursor.execute("CREATE USER IF NOT EXISTS 'flask_user'@'%' IDENTIFIED BY '555555';")
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

        # users 테이블 생성
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

        # saramin_jobs 테이블 생성
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS saramin_jobs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                company VARCHAR(255) NOT NULL,
                title VARCHAR(255) NOT NULL,
                location VARCHAR(255) DEFAULT NULL,
                salary VARCHAR(100) DEFAULT NULL,
                link TEXT NOT NULL,
                education VARCHAR(100) DEFAULT NULL,
                description TEXT DEFAULT NULL,
                employment_type VARCHAR(100) DEFAULT NULL,
                experience VARCHAR(100) DEFAULT NULL,
                deadline DATE DEFAULT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # favorites 테이블 생성
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                job_id INT NOT NULL,
                applied BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (job_id) REFERENCES saramin_jobs(id) ON DELETE CASCADE
            );
        """)

        # logs 테이블 생성
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                log_message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
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
