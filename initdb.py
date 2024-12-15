import pymysql
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv  # .env 파일 로드
import os  # 환경변수 접근

# .env 파일 로드
load_dotenv()

# MySQL 데이터베이스 설정 (환경변수에서 로드)
db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "charset": os.getenv("DB_CHARSET", "utf8mb4"),
    "cursorclass": pymysql.cursors.DictCursor    
}

def setup_database():
    conn = None
    cursor = None    
    try:
        # MySQL 데이터베이스 연결
        conn = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"]
        )
        cursor = conn.cursor()

        # 데이터베이스 삭제
        #cursor.execute("DROP DATABASE IF EXISTS saramin_db;")
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
        # MySQL 데이터베이스 연결
        conn = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"]
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
            link TEXT NOT NULL,                           
            location VARCHAR(255) DEFAULT NULL,       
            experience VARCHAR(100) DEFAULT NULL,         
            education VARCHAR(100) DEFAULT NULL,      
            employment_type VARCHAR(100) DEFAULT NULL,    
            description TEXT DEFAULT NULL,                
            deadline DATE DEFAULT NULL,                   
            salary VARCHAR(100) DEFAULT NULL,             
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # bookmarks 테이블 생성
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookmarks (
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

        # 이력서 테이블 생성
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS _resume (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                _resume_ TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            );
        """)

        # 리뷰 테이블 생성
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS _review (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                job_id INT NOT NULL,
                review_score INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (job_id) REFERENCES saramin_jobs(id) ON DELETE CASCADE
            );
        """)
        
        
        # 사용자의 회사 추가 정보
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS _user_opinion (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                job_id INT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (job_id) REFERENCES saramin_jobs(id) ON DELETE CASCADE
            );
        """)
        
        # 사용자 게시판
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS _user_board (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                board TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            );
        """)        

        print("Tables created successfully.")

        # 테이블 출력
        print("\n========== TABLES IN saramin_db ==========")
        cursor.execute("SHOW TABLES;")
        for table in cursor.fetchall():
            print(table[0])

        # users 테이블 구조 출력
        print("\n========== STRUCTURE OF users TABLE ==========")
        cursor.execute("DESCRIBE users;")
        for row in cursor.fetchall():
            print(row)

        # saramin_jobs 테이블 구조 출력
        print("\n========== STRUCTURE OF saramin_jobs TABLE ==========")
        cursor.execute("DESCRIBE saramin_jobs;")
        for row in cursor.fetchall():
            print(row)

        # logs 테이블 구조 출력
        print("\n========== STRUCTURE OF logs TABLE ==========")
        cursor.execute("DESCRIBE logs;")
        for row in cursor.fetchall():
            print(row)
            
        print("\n========== STRUCTURE OF _resume TABLE ==========")
        cursor.execute("DESCRIBE _resume;")
        for row in cursor.fetchall():
            print(row)            
            
        print("\n========== STRUCTURE OF _review TABLE ==========")
        cursor.execute("DESCRIBE _review;")
        for row in cursor.fetchall():
            print(row)            
            
        print("\n========== STRUCTURE OF _user_opinion TABLE ==========")
        cursor.execute("DESCRIBE _user_opinion;")
        for row in cursor.fetchall():
            print(row)            
            
        print("\n========== STRUCTURE OF _user_board TABLE ==========")
        cursor.execute("DESCRIBE _user_board;")
        for row in cursor.fetchall():
            print(row)                                                

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
