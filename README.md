# Crawler 

## 웹서비스 설계 과제3

### .env 설정
 * 다음과 같이 시험 환경에 맞춰 DB, SWAGGER 정보를 설정
```c
# 데이터베이스 설정
DB_HOST=localhost
DB_PORT=3000
DB_USER=flask_user
DB_PASSWORD=555555
DB_NAME=saramin_db
DB_CHARSET=utf8mb4
DB_CURSORCLASS=pymysql.cursors.DictCursor

# Swagger 설정
SWAGGER_HOST=192.168.209.132:8080
```
### 파이썬 가상환경 환경 설정
 * python 가상환경 설정
```c
python3 -m venv ../flask_env
source ../flask_env/bin/activate
pip install -r requirements.txt
```   

### MYSQL 최초 계정 등록
  * 최초 설치시에는 아무런 계정이 없으므로, root와 flask_user 계정을 생성함
  * root는 관리용, flask_user는 앱 개발용임
```c
sudo mysql

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '555555';
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '555555';

ALTER USER 'flask_user'@'localhost' IDENTIFIED WITH mysql_native_password BY '555555';
ALTER USER 'flask_user'@'%' IDENTIFIED WITH mysql_native_password BY '555555';

FLUSH PRIVILEGES;
commit;

```  
  * **MYSQL 데이터베이스(모델) 생성**
```c
python initdb.py
Database and user setup completed successfully.
Tables created successfully.

========== TABLES IN saramin_db ==========
_resume
_review
favorites
logs
recruiter
saramin_jobs
user_notifications
users

========== STRUCTURE OF users TABLE ==========
('id', 'int', 'NO', 'PRI', None, 'auto_increment')
('user_id', 'varchar(255)', 'NO', 'UNI', None, '')
('email', 'varchar(255)', 'NO', 'UNI', None, '')
('password', 'varchar(255)', 'NO', '', None, '')
('name', 'varchar(255)', 'NO', '', None, '')
('created_at', 'timestamp', 'YES', '', 'CURRENT_TIMESTAMP', 'DEFAULT_GENERATED')

========== STRUCTURE OF saramin_jobs TABLE ==========
('id', 'int', 'NO', 'PRI', None, 'auto_increment')
('company', 'varchar(255)', 'NO', '', None, '')
('title', 'varchar(255)', 'NO', '', None, '')
('link', 'text', 'NO', '', None, '')
('location', 'varchar(255)', 'YES', '', None, '')
('experience', 'varchar(100)', 'YES', '', None, '')
('education', 'varchar(100)', 'YES', '', None, '')
('employment_type', 'varchar(100)', 'YES', '', None, '')
('description', 'text', 'YES', '', None, '')
('deadline', 'date', 'YES', '', None, '')
('salary', 'varchar(100)', 'YES', '', None, '')
('created_at', 'timestamp', 'YES', '', 'CURRENT_TIMESTAMP', 'DEFAULT_GENERATED')

========== STRUCTURE OF logs TABLE ==========
('id', 'int', 'NO', 'PRI', None, 'auto_increment')
('user_id', 'varchar(255)', 'NO', 'MUL', None, '')
('log_message', 'text', 'NO', '', None, '')
('created_at', 'timestamp', 'YES', '', 'CURRENT_TIMESTAMP', 'DEFAULT_GENERATED')

========== STRUCTURE OF _resume TABLE ==========
('id', 'int', 'NO', 'PRI', None, 'auto_increment')
('user_id', 'varchar(255)', 'NO', 'MUL', None, '')
('_resume_', 'text', 'NO', '', None, '')
('created_at', 'timestamp', 'YES', '', 'CURRENT_TIMESTAMP', 'DEFAULT_GENERATED')

========== STRUCTURE OF _review TABLE ==========
('id', 'int', 'NO', 'PRI', None, 'auto_increment')
('user_id', 'varchar(255)', 'NO', 'MUL', None, '')
('job_id', 'int', 'NO', 'MUL', None, '')
('review_score', 'int', 'NO', '', None, '')
('created_at', 'timestamp', 'YES', '', 'CURRENT_TIMESTAMP', 'DEFAULT_GENERATED')
(중략)

```
  * **크롤러 실행(로그 생성)**
    * 클로러를 실행하면 saramin_python.csv를 로컬에 만들고, DB에도 저장함
```c
python crawl_saramin.py
2024-12-15 13:50:35,412 [INFO] 데이터베이스가 성공적으로 초기화되었습니다.
2024-12-15 13:50:35,412 [INFO] 일일 크롤링 시작: 2024-12-15 13:50:35.412444
2024-12-15 13:50:35,412 [INFO] 앱 실행 중...
2024-12-15 13:50:35,412 [INFO] 1 페이지 크롤링 중...
2024-12-15 13:50:40,154 [INFO] 2 페이지 크롤링 중...
2024-12-15 13:50:45,990 [INFO] 3 페이지 크롤링 중...
2024-12-15 13:50:51,979 [INFO] 4 페이지 크롤링 중...
2024-12-15 13:50:56,265 [INFO] 총 110개의 채용 공고를 크롤링했습니다.
2024-12-15 13:50:56,306 [INFO] 100개의 데이터를 데이터베이스에 저장했습니다.
2024-12-15 13:50:56,307 [INFO] 100개의 데이터를 saramin_python.csv 파일에 저장했습니다.
2024-12-15 13:50:56,308 [INFO] 크롤링 완료. 다음 크롤링은 24시간 후.
```
 * **flask app 백그라운드 실행**
```c
chmod +x app_start.sh
./app_start.sh
Stale PID file found. Removing it...
Starting Flask App...
Flask App started with PID 4653
```

  * **flask app 백그라운드 종료**
```c
chmod +x app_stop.sh
./app_stop.sh
Stopping Flask App with PID 4653...
Flask App stopped.
```

### Swagger 문서

- Swagger UI 주소: [http://113.198.66.75:10018/api-docs/](http://113.198.66.75:10018/api-docs/)

#### Swagger 문서 확인 방법
1. 서버를 시작한 후 브라우저에서 아래 주소로 접속:
   ```
   http://<your-server>:<port>/api-docs
   ```
2. API 목록을 확인하고 테스트할 수 있습니다.

### 기술 스택

- **Database**: MySQL
- **Backend Framework**: Flask
- **API Documentation**: Swagger
- **Authentication**: JWT

### 📂 프로젝트 폴더 구조

```plaintext
├── 📂 src                  # 주요 소스 코드 디렉토리
│   ├── 🟨 app.py               # flask 애플리케이션의 진입점 스크립트    
│   ├── 🟨 applications.py      # 지원서 관련 APi 라우트 스크립트
│   ├── 🟨 auth.py              # auth 관련 API 라우트 스크립트
│   ├── 🟨 bookmarks.py         # 북마크 관련 API 라우트 스크립트
│   ├── 🟨 jobs.py              # 채용공고 관련 API 라우트 스크립트
│   ├── 🟨 resume.py            # 이력서 관련 API 라우트 스크립트
│   ├── 🟨 review.py            # 리뷰 관련 API 라우트 스크립트
│   ├── 🟨 opinion.py           # 사용자 의견 관련 API 라우트 스크립트
│   ├── 🟨 board.py             # 게시판 관련 API 라우트 스크립트
│   └── 🟨 db.py                # DB 접속 정보(.env) 로드 및 접속 스크립트
├── 📄 .env                 # 환경 변수 파일
├── 📄 crawler.log          # 로그 파일
├── 🐍 crawl_saramin.py     # 사람인 크롤러 스크립트
├── 🟨 requirements.txt     # 파이썬 의존성 모듈 목록 파일
├── 🟨 saramin_python.csv   # 크롤러가 생성한 사람인 DB
├── 🟨 initdb.py            # MYSQL 사용자, 북마크, 채용 공고 등 모델 8개 초기화/생성 스크립트
├── 🟨 csv2db.py            # 로컬 .csv -> MYSQL DB(saramin_db) 저장 스크립트
├── 🟨 app_start.sh         # flask 애플리케이션 백그라운드 실행 스크립트
├── 🟨 app_stop.sh          # flask 애플리케이션 종료 스크립트
├── 🟨 flask_app.log        # flask 애플리케이션 실행 로그
└── 🟦 README.md            # 프로젝트 설명 파일
```


# API 소개

## Apply(지원 관련 API)
- **POST** `​/applications` : 지원 등록
- **DELETE** `​/applications/cancel` : 지원 취소
- **GET** `/applications/list/{user_id}` : 지원 목록 조회
---
## Authentication(회원가입/로그인 관련 API)  
- **POST** `​/auth/login` : 로그인
- **PUT** `/auth/profile/change_password/{user_id}` : 비밀번호 변경
- **GET** `/auth/profile/{user_id}` : 회원 정보 조회
- **POST** `/auth/register` : 회원 가입
- **DELETE** `/autu/profile/{user_id}` : 회원 탈퇴
- **PUT** `/autu/profile/{user_id}` : 회원 정보 수정
---
## User Board(게시판 관련 API)
- **GET** `​/board` : 게시글 조회
- **POST** `/board` : 게시글 등록
- **DELETE** `/board/{id}` : 게시글 삭제
---
## Bookmarks(북마크 관련 API)
- **POST** `/bookmarks` : 관심 등록
- **GET** `/bookmarks/{user_id}` : 관심 채용 공고 조회
---
## Job Posting(채용공고 관련 API)
- **GET** `/jobs` : 채용 공고 목록 조회 API
- **POST** `/jobs` : 채용 공고 등록 API
- **DELETE** `/jobs/{job_id}` : 채용 공고 삭제 API
- **GET** `/jobs/{job_id}` : 채용 공고 상세 조회 API
- **PUT** `/jobs/{job_id}` : 채용 공고 수정 API
---
## User Opinion(사용자 의견 관련 API)
- **POST** `/opinon` : 사용자 의견 등록 API
- **DELETE** `/opinon/{id}` : 사용자 의견 삭제 API
- **GET** `/opinon/{job_id}` : 사용자 의견 조회 API
---
## RESUME(이력서 관련 API)
- **POST** `/resume` : 이력서 등록 API
- **GET** `/resume/{user_id}` : 이력서 조회 API
---
## Review(채용 공고 리뷰 관련 API)
- **POST** `/revew` : 리뷰 등록 API
- **GET** `/revew/{job_id}` : 리뷰 조회 API

# 기타 설정
## mysql 외부 접속 허용 및 포트 수정
### 1) mysqld.cnf 수정
sudo vi /etc/mysql/mysql.conf.d/mysqld.cnf
#port = 3306
port = 3000
bind-address = 0.0.0.0

재시작
sudo systemctl restart mysql
재시작 후 안 되면 2) 적용 후 재시작

### 2) mysql.cnf 수정
sudo vi /etc/mysql/mysql.cnf 에 아래 라인 추가

[mysqld]			            # 추가
#port=3306 # or any other port	# 추가
port=3000 # or any other port	# 추가
bind-address=0.0.0.0		    # 추가

재시작
sudo systemctl restart mysql