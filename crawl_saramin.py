import requests
from bs4 import BeautifulSoup
import pymysql
import time
from datetime import datetime
import threading
import logging
import csv  # CSV 파일 저장을 위한 모듈
import random
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("crawler.log")
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

# 여러 User-Agent 목록 (로테이션 사용)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
]

# 세션 생성 (재시도 로직 포함)
def get_session():
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session

# 데이터베이스 초기화 함수
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
            for job in jobs:
                cursor.execute(insert_query, (
                    job["company"], job["title"], job["link"], job["location"],
                    job["experience"], job["education"], job["employment_type"],
                    job["description"], job["deadline"], job["salary"]
                ))
            connection.commit()
        logging.info(f"{len(jobs)}개의 데이터를 데이터베이스에 저장했습니다.")
    except pymysql.MySQLError as e:
        logging.error(f"데이터베이스 저장 중 에러 발생: {e}")
    finally:
        if connection:
            connection.close()

    save_to_csv(jobs)

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

# 크롤링 페이지 함수
def crawl_page(keyword, page, session, visited_companies):
    url = f"https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword={keyword}&recruitPage={page}"
    jobs = []
    try:
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        job_listings = soup.select(".item_recruit")

        for job in job_listings:
            try:
                company = job.select_one(".corp_name a").text.strip()
                if company in visited_companies:
                    continue
                visited_companies.add(company)

                title = job.select_one(".job_tit a").text.strip()
                link = "https://www.saramin.co.kr" + job.select_one(".job_tit a")["href"]
                location = job.select_one(".job_condition span").text.strip() if job.select_one(".job_condition span") else ""
                experience = job.select_one(".job_condition span:nth-child(2)").text.strip() if job.select_one(".job_condition span:nth-child(2)") else ""
                education = job.select_one(".job_condition span:nth-child(3)").text.strip() if job.select_one(".job_condition span:nth-child(3)") else ""
                employment_type = job.select_one(".job_condition span:nth-child(4)").text.strip() if job.select_one(".job_condition span:nth-child(4)") else ""
                description = job.select_one(".job_sector").text.strip() if job.select_one(".job_sector") else ""
                raw_deadline = job.select_one(".job_date .date").text.strip() if job.select_one(".job_date .date") else ""
                deadline = parse_deadline(raw_deadline)
                salary = job.select_one(".area_badge .badge").text.strip() if job.select_one(".area_badge .badge") else ""

                jobs.append({
                    "company": company, "title": title, "link": link, "location": location,
                    "experience": experience, "education": education, "employment_type": employment_type,
                    "description": description, "deadline": deadline, "salary": salary
                })
            except AttributeError:
                continue
    except requests.RequestException as e:
        logging.error(f"{page} 페이지 요청 중 에러 발생: {e}")
    return jobs

# 크롤링한 데이터를 CSV 파일로 저장하는 함수
def save_to_csv(jobs):
    csv_file = "saramin_python.csv"
    try:
        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=[
                "company", "title", "link", "location", "experience", "education", 
                "employment_type", "description", "deadline", "salary"
            ])
            writer.writeheader()
            writer.writerows(jobs)
        logging.info(f"{len(jobs)}개의 데이터를 {csv_file} 파일에 저장했습니다.")
    except Exception as e:
        logging.error(f"CSV 파일 저장 중 에러 발생: {e}")

# 전체 채용 공고를 크롤링하는 함수
def crawl_saramin(keyword="python", min_jobs=100):
    session = get_session()
    jobs = []
    visited_companies = set()
    page = 1

    while len(jobs) < min_jobs:
        logging.info(f"{page} 페이지 크롤링 중...")
        jobs.extend(crawl_page(keyword, page, session, visited_companies))
        page += 1
        time.sleep(random.uniform(2, 5))  # 서버 부하 방지를 위한 랜덤 지연

    logging.info(f"총 {len(jobs)}개의 채용 공고를 크롤링했습니다.")
    save_to_database(jobs[:min_jobs])

# 매일 한 번 크롤링하는 스케줄러
def schedule_daily_crawl():
    while True:
        logging.info(f"일일 크롤링 시작: {datetime.now()}")
        crawl_saramin(min_jobs=100)
        logging.info("크롤링 완료. 다음 크롤링은 24시간 후.")
        time.sleep(86400)

# 메인 실행
if __name__ == "__main__":
    initialize_database()
    threading.Thread(target=schedule_daily_crawl, daemon=True).start()
    logging.info("앱 실행 중...")
    while True:
        time.sleep(1)
