import pymysql
from dotenv import load_dotenv  # .env 파일 로드
import os  # 환경변수 접근

# .env 파일 로드
load_dotenv()

# MySQL 데이터베이스 설정 (환경변수에서 로드)
db_config = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "charset": os.getenv("DB_CHARSET", "utf8mb4"),
    "cursorclass": pymysql.cursors.DictCursor    
}


# MySQL 연결 함수
def get_db_connection():
    return pymysql.connect(**db_config)
