import pymysql

# MySQL 연결 설정
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='your_root_password',
    database='mysql',  # 기본 MySQL 데이터베이스
)

# SQL 파일 실행
with open('db_create.sql', 'r') as file:
    sql_script = file.read()

try:
    with connection.cursor() as cursor:
        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)
    connection.commit()
    print("SQL 스크립트 실행 완료")
finally:
    connection.close()
