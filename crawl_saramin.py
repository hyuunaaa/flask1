import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
from concurrent.futures import ThreadPoolExecutor

# 데이터 무결성을 위한 중복 제거용 집합
visited_links = set()

def crawl_page(keyword, page, headers):
    """
    특정 페이지의 채용 정보를 크롤링하는 함수.

    Args:
        keyword (str): 검색 키워드
        page (int): 페이지 번호
        headers (dict): 요청 헤더

    Returns:
        list: 채용 공고 정보 리스트
    """
    url = f"https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword={keyword}&recruitPage={page}"
    jobs = []

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        job_listings = soup.select('.item_recruit')

        for job in job_listings:
            try:
                # 회사명
                company = job.select_one('.corp_name a').text.strip()
                # 채용 제목
                title = job.select_one('.job_tit a').text.strip()
                # 채용 링크
                link = 'https://www.saramin.co.kr' + job.select_one('.job_tit a')['href']

                # 중복 확인
                if link in visited_links:
                    continue
                visited_links.add(link)

                # 지역, 경력, 학력, 고용형태
                conditions = job.select('.job_condition span')
                location = conditions[0].text.strip() if len(conditions) > 0 else ''
                experience = conditions[1].text.strip() if len(conditions) > 1 else ''
                education = conditions[2].text.strip() if len(conditions) > 2 else ''
                employment_type = conditions[3].text.strip() if len(conditions) > 3 else ''

                # 마감일
                deadline = job.select_one('.job_date .date').text.strip()
                # 직무 분야
                job_sector = job.select_one('.job_sector')
                sector = job_sector.text.strip() if job_sector else ''
                # 평균연봉 정보 (있는 경우)
                salary_badge = job.select_one('.area_badge .badge')
                salary = salary_badge.text.strip() if salary_badge else ''

                jobs.append({
                    '회사명': company,
                    '제목': title,
                    '링크': link,
                    '지역': location,
                    '경력': experience,
                    '학력': education,
                    '고용형태': employment_type,
                    '마감일': deadline,
                    '직무분야': sector,
                    '연봉정보': salary
                })

            except AttributeError as e:
                print(f"항목 파싱 중 에러 발생: {e}")
                continue

    except requests.RequestException as e:
        print(f"페이지 요청 중 에러 발생: {e}")

    return jobs


def crawl_saramin(keyword, pages=1, min_jobs=100):
    """
    사람인 채용공고를 크롤링하는 함수.

    Args:
        keyword (str): 검색할 키워드
        pages (int): 초기 크롤링할 페이지 수
        min_jobs (int): 최소 크롤링할 데이터 수

    Returns:
        DataFrame: 채용공고 정보가 담긴 데이터프레임
    """
    jobs = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    page = 1
    while len(jobs) < min_jobs:
        print(f"{page} 페이지 크롤링 중...")
        jobs.extend(crawl_page(keyword, page, headers))
        page += 1
        time.sleep(1)  # 서버 부하 방지 딜레이

    print(f"총 {len(jobs)}개의 채용 공고를 크롤링했습니다.")
    return pd.DataFrame(jobs[:min_jobs])  # 최소 요구 개수만 반환


def crawl_parallel(keyword, pages=10):
    """
    병렬 처리로 여러 페이지를 동시에 크롤링하는 함수.

    Args:
        keyword (str): 검색할 키워드
        pages (int): 크롤링할 페이지 수

    Returns:
        DataFrame: 채용공고 정보가 담긴 데이터프레임
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    jobs = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(lambda page: crawl_page(keyword, page, headers), range(1, pages + 1))
        for result in results:
            jobs.extend(result)

    print(f"병렬 처리로 총 {len(jobs)}개의 채용 공고를 크롤링했습니다.")
    return pd.DataFrame(jobs)


# 사용 예시
if __name__ == "__main__":
    # 'python' 키워드로 3페이지 크롤링
    df = crawl_saramin('python', pages=5, min_jobs=100)
    print(df)
    df.to_csv('saramin_python.csv', index=False)
