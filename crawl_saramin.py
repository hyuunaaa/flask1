import requests
from bs4 import BeautifulSoup
import pymysql
import time
from datetime import datetime
import threading
import logging
import csv  # CSV 파일 저장을 위한 모듈

# 로깅 설정: 화면과 파일에 로그 기록
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),  # 콘솔 출력 핸들러
        logging.FileHandler("crawler.log")  # 파일 출력 핸들러
    ]
)

# MySQL 데이터베이스 설정
db_config = {
    "host": "localhost",
    "user": "flask_user",
    "password": "555555",
    "database": "saramin_db",
    "charset": "utf8mb4"
}

# 데이터베이스 초기화 함수: 데이터베이스가 없는 경우 생성
def initialize_database():
    try:
        conn = pymysql.connect(host=db_config["host"], user=db_config["user"], password=db_config["password"])
        with conn.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS saramin_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;")
        logging.info("데이터베이스가 성공적으로 초기화되었습니다.")
    except pymysql.MySQLError as e:
        logging.error(f"데이터베이스 초기화 중 에러 발생: {e}")
    finally:
        if conn:
            conn.close()

# 데이터베이스에 크롤링한 데이터를 저장하는 함수
def save_to_database(jobs):
    connection = None
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # saramin_jobs 테이블에 데이터 삽입 쿼리
            insert_query = """
            INSERT INTO saramin_jobs (title, company, location, salary, description, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
            ON DUPLICATE KEY UPDATE
            location=VALUES(location),
            salary=VALUES(salary),
            description=VALUES(description);
            """
            for job in jobs:
                cursor.execute(insert_query, (
                    job["title"],
                    job["company"],
                    job["location"],
                    job["salary"],
                    job["description"],
                ))
            connection.commit()
        logging.info(f"{len(jobs)}개의 데이터를 데이터베이스에 저장했습니다.")
    except pymysql.MySQLError as e:
        logging.error(f"데이터베이스 저장 중 에러 발생: {e}")
    finally:
        if connection:
            connection.close()

    # CSV 파일로 저장하는 부분 추가
    save_to_csv(jobs)

# 특정 페이지의 채용 정보를 크롤링하는 함수
def crawl_page(keyword, page, headers, visited_companies):
    """
    Args:
        keyword (str): 검색할 키워드
        page (int): 크롤링할 페이지 번호
        headers (dict): HTTP 요청 헤더
        visited_companies (set): 이미 방문한 회사 목록

    Returns:
        list: 채용 공고 정보 리스트
    """
    url = f"https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword={keyword}&recruitPage={page}"
    jobs = []

    try:
        # 페이지 요청
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        job_listings = soup.select(".item_recruit")

        for job in job_listings:
            try:
                # 회사명 파싱
                company = job.select_one(".corp_name a").text.strip()
                if company in visited_companies:
                    continue  # 이미 방문한 회사는 스킵
                visited_companies.add(company)

                # 나머지 정보 파싱
                title = job.select_one(".job_tit a").text.strip()
                location = job.select_one(".job_condition span").text.strip() if job.select_one(".job_condition span") else ""
                salary = job.select_one(".area_badge .badge").text.strip() if job.select_one(".area_badge .badge") else ""
                description = job.select_one(".job_sector").text.strip() if job.select_one(".job_sector") else ""

                # 크롤링한 데이터 리스트에 추가
                jobs.append({
                    "company": company,
                    "title": title,
                    "location": location,
                    "salary": salary,
                    "description": description,
                })
            except AttributeError as e:
                logging.warning(f"공고 파싱 중 에러 발생: {e}")
    except requests.RequestException as e:
        logging.error(f"{page} 페이지 요청 중 에러 발생: {e}")

    return jobs

# 크롤링한 데이터를 CSV 파일로 저장하는 함수
def save_to_csv(jobs):
    csv_file = "saramin_python.csv"
    try:
        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["company", "title", "location", "salary", "description"])
            writer.writeheader()  # CSV 파일의 헤더 작성
            writer.writerows(jobs)  # 데이터 작성
        logging.info(f"{len(jobs)}개의 데이터를 {csv_file} 파일에 저장했습니다.")
    except Exception as e:
        logging.error(f"CSV 파일 저장 중 에러 발생: {e}")

# 전체 채용 공고를 크롤링하는 함수
def crawl_saramin(keyword="python", min_jobs=100):
    """
    Args:
        keyword (str): 검색 키워드
        min_jobs (int): 최소 크롤링할 공고 수
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    jobs = []
    visited_companies = set()
    page = 1

    # 최소 크롤링 데이터를 충족할 때까지 반복
    while len(jobs) < min_jobs:
        logging.info(f"{page} 페이지 크롤링 중...")
        jobs.extend(crawl_page(keyword, page, headers, visited_companies))
        page += 1
        time.sleep(1)  # 서버 부하 방지 딜레이

    logging.info(f"총 {len(jobs)}개의 채용 공고를 크롤링했습니다.")
    save_to_database(jobs[:min_jobs])  # 최소 요구 데이터 저장

# 매일 한 번 크롤링하는 스케줄러
def schedule_daily_crawl():
    while True:
        logging.info(f"일일 크롤링 시작: {datetime.now()}")
        crawl_saramin(min_jobs=100)
        logging.info("크롤링 완료. 다음 크롤링은 24시간 후.")
        time.sleep(86400)  # 24시간 대기

if __name__ == "__main__":
    initialize_database()  # 데이터베이스 초기화
    # 크롤링 스레드 시작
    threading.Thread(target=schedule_daily_crawl, daemon=True).start()

    logging.info("앱 실행 중. 백그라운드에서 크롤링 진행 중...")
    while True:
        time.sleep(1)
