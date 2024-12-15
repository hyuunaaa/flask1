# Crawler

## 웹서비스 설계 과제3


### 파이썬 가상환경 환경 설정
  * python 가상환경 설정
```c
python3 -m venv ../flask_env
source ../flask_env/bin/activate
pip install -r requirements.txt
```   

### MYSQL 최초 계정 등록
  * 최초 설치시에는 아무런 계정이 없으므로, root와 flask_user 계정을 생성함
  * root는 관리용, flas_user는 앱 개발용임
```c
sudo mysql

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '555555';
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '555555';

ALTER USER 'flask_user'@'localhost' IDENTIFIED WITH mysql_native_password BY '555555';
ALTER USER 'flask_user'@'%' IDENTIFIED WITH mysql_native_password BY '555555';

FLUSH PRIVILEGES;
commit;

```  
  * **MYSQL 데이터베이스 생성**
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

========== STRUCTURE OF recruiter TABLE ==========
('id', 'int', 'NO', 'PRI', None, 'auto_increment')
('user_id', 'varchar(255)', 'NO', 'UNI', None, '')
('email', 'varchar(255)', 'NO', 'UNI', None, '')
('password', 'varchar(255)', 'NO', '', None, '')
('name', 'varchar(255)', 'NO', '', None, '')
('created_at', 'timestamp', 'YES', '', 'CURRENT_TIMESTAMP', 'DEFAULT_GENERATED')

========== STRUCTURE OF user_notifications TABLE ==========
('id', 'int', 'NO', 'PRI', None, 'auto_increment')
('recruiter_id', 'varchar(255)', 'NO', 'MUL', None, '')
('user_id', 'varchar(255)', 'NO', 'MUL', None, '')
('message', 'text', 'NO', '', None, '')
('created_at', 'datetime', 'YES', '', 'CURRENT_TIMESTAMP', 'DEFAULT_GENERATED')
(flask_env) (base) root@DESKTOP-E2ELUTD:/home/memtest/study/recruit/flask1# python initdb.py
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

========== STRUCTURE OF recruiter TABLE ==========
('id', 'int', 'NO', 'PRI', None, 'auto_increment')
('user_id', 'varchar(255)', 'NO', 'UNI', None, '')
('email', 'varchar(255)', 'NO', 'UNI', None, '')
('password', 'varchar(255)', 'NO', '', None, '')
('name', 'varchar(255)', 'NO', '', None, '')
('created_at', 'timestamp', 'YES', '', 'CURRENT_TIMESTAMP', 'DEFAULT_GENERATED')

========== STRUCTURE OF user_notifications TABLE ==========
('id', 'int', 'NO', 'PRI', None, 'auto_increment')
('recruiter_id', 'varchar(255)', 'NO', 'MUL', None, '')
('user_id', 'varchar(255)', 'NO', 'MUL', None, '')
('message', 'text', 'NO', '', None, '')
('created_at', 'datetime', 'YES', '', 'CURRENT_TIMESTAMP', 'DEFAULT_GENERATED')
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