import csv
import pymysql
import logging
from dotenv import load_dotenv
import os
import argparse
from datetime import datetime

# .env 파일 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# MySQL 데이터베이스 설정 (환경변수에서 로드)
db_config = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),  # 포트를 정수로 변환
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "charset": os.getenv("DB_CHARSET", "utf8mb4"),
    "cursorclass": pymysql.cursors.DictCursor
}

# 문자열 마감일을 MySQL DATE 형식으로 변환하는 함수
def parse_deadline(raw_deadline):
    """
    문자열 형식의 마감일을 MySQL DATE 형식으로 변환.
    Args:
        raw_deadline (str): 크롤링된 마감일 문자열 (예: "~ 12/31(화)")
    Returns:
        str: 변환된 'YYYY-MM-DD' 형식의 날짜 또는 None
    """
    try:
        # "~ 12/31(화)" 또는 "~ 01/09(목)" 형태를 처리
        cleaned_deadline = raw_deadline.replace("~", "").strip().split("(")[0]
        parsed_date = datetime.strptime(f"2024/{cleaned_deadline}", "%Y/%m/%d")  # 연도는 2024로 가정
        return parsed_date.strftime("%Y-%m-%d")
    except (ValueError, AttributeError):
        return None

# saramin_python2.csv 데이터를 데이터베이스에 추가
def add_csv_to_database(csv_file_path):
    connection = None  # 초기화
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            insert_query = """
            INSERT INTO saramin_jobs (
                company, title, link, location, experience, education, 
                employment_type, description, deadline, salary, created_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            ON DUPLICATE KEY UPDATE
            location=VALUES(location),
            experience=VALUES(experience),
            education=VALUES(education),
            employment_type=VALUES(employment_type),
            description=VALUES(description),
            deadline=VALUES(deadline),
            salary=VALUES(salary);
            """
            with open(csv_file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                success_count = 0
                error_count = 0

                for row in reader:
                    try:
                        cursor.execute(insert_query, (
                            row["company"], row["title"], row["link"], row["location"],
                            row["experience"], row["education"], row["employment_type"],
                            row["description"], parse_deadline(row["deadline"]), row["salary"]
                        ))
                        success_count += 1
                    except pymysql.IntegrityError as e:
                        logging.warning(f"Integrity error for company '{row['company']}': {e}")
                        error_count += 1
                    except pymysql.MySQLError as e:
                        logging.error(f"MySQL error for company '{row['company']}': {e}")
                        error_count += 1

                connection.commit()

        logging.info(f"{success_count}개의 레코드가 성공적으로 추가되었습니다.")
        logging.info(f"{error_count}개의 레코드에서 오류가 발생했습니다.")

    except pymysql.MySQLError as e:
        logging.error(f"데이터베이스 작업 중 에러 발생: {e}")
    except Exception as e:
        logging.error(f"일반 에러 발생: {e}")
    finally:
        if connection:  # connection 변수가 None이 아닌 경우에만 닫음
            connection.close()

if __name__ == "__main__":
    # 명령행 인자 설정
    parser = argparse.ArgumentParser(description="Add CSV data to saramin_jobs table.")
    parser.add_argument("csv_file", help="Path to the CSV file (e.g., saramin_python2.csv)")
    args = parser.parse_args()

    # CSV 파일 경로 가져오기
    csv_file_path = args.csv_file
    logging.info(f"Provided CSV file: {csv_file_path}")

    # CSV 데이터를 데이터베이스에 추가
    add_csv_to_database(csv_file_path)
