# Crawler

## 웹서비스 설계 과제3

### 설치 및 실행 방법
  * MYSQL 계정 생성
```c
sudo mysql

mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '555555';
Query OK, 0 rows affected (0.00 sec)

mysql> ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '555555';
Query OK, 0 rows affected (0.00 sec)

mysql> ALTER USER 'flask_user'@'localhost' IDENTIFIED WITH mysql_native_password BY '555555';
mysql> ALTER USER 'flask_user'@'%' IDENTIFIED WITH mysql_native_password BY '555555';

mysql> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.01 sec)

mysql> commit;
Query OK, 0 rows affected (0.00 sec)
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
