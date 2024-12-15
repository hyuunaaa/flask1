import pymysql

# MySQL 데이터베이스 연결 설정
db_config = {
    "host": "localhost",
    "user": "flask_user",
    "password": "555555",
    "database": "saramin_db",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor
}

# MySQL 연결 함수
def get_db_connection():
    return pymysql.connect(**db_config)
