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
mysql -u root -p < ./crawled-data.sql
Enter password:

Section
*** DATABASES LIST ***
Database
information_schema
mysql
performance_schema
saramin_db
sys
Section
*** MYSQL USERS ***
user    host
flask_user      %
root    %
debian-sys-maint        localhost
flask_user      localhost
mysql.infoschema        localhost
mysql.session   localhost
mysql.sys       localhost
root    localhost
Output
========== TABLES IN saramin_db ==========
Tables_in_saramin_db
apply_
favorites
logs
saramin_jobs 
users
Section
========== STRUCTURE OF users TABLE ==========
Field   Type    Null    Key     Default Extra
id      int     NO      PRI     NULL    auto_increment
user_id varchar(255)    NO      UNI     NULL
email   varchar(255)    NO      UNI     NULL
password        varchar(255)    NO              NULL
name    varchar(255)    NO              NULL
created_at      timestamp       YES             CURRENT_TIMESTAMP       DEFAULT_GENERATED
Section
========== STRUCTURE OF saramin_jobs TABLE ==========
Field   Type    Null    Key     Default Extra
id      int     NO      PRI     NULL    auto_increment
title   varchar(255)    NO              NULL
company varchar(255)    NO              NULL
location        varchar(255)    NO              NULL
salary  varchar(255)    YES             NULL
description     text    YES             NULL
created_at      timestamp       YES             CURRENT_TIMESTAMP       DEFAULT_GENERATED
Section
========== STRUCTURE OF favorites TABLE ==========
Field   Type    Null    Key     Default Extra
id      int     NO      PRI     NULL    auto_increment
user_id varchar(255)    NO      MUL     NULL
job_id  int     NO      MUL     NULL
applied tinyint(1)      YES             0
created_at      timestamp       YES             CURRENT_TIMESTAMP       DEFAULT_GENERATED
Section
========== STRUCTURE OF logs TABLE ==========
Field   Type    Null    Key     Default Extra
id      int     NO      PRI     NULL    auto_increment
user_id varchar(255)    NO      MUL     NULL
log_message     text    NO              NULL
created_at      timestamp       YES             CURRENT_TIMESTAMP       DEFAULT_GENERATED
```
  * **크롤러 실행(로그 생성)**
```c
python crawl_saramin.py
2024-12-15 09:38:44,885 [INFO] 데이터베이스가 성공적으로 초기화되었습니다.
2024-12-15 09:38:44,885 [INFO] 일일 크롤링 시작: 2024-12-15 09:38:44.885452
2024-12-15 09:38:44,885 [INFO] 앱 실행 중. 백그라운드에서 크롤링 진행 중...
2024-12-15 09:38:44,885 [INFO] 1 페이지 크롤링 중...
2024-12-15 09:38:46,968 [INFO] 2 페이지 크롤링 중...
2024-12-15 09:38:49,023 [INFO] 3 페이지 크롤링 중...
2024-12-15 09:38:51,077 [INFO] 총 106개의 채용 공고를 크롤링했습니다.
2024-12-15 09:38:51,130 [INFO] 100개의 데이터를 데이터베이스에 저장했습니다.
2024-12-15 09:38:51,131 [INFO] 100개의 데이터를 saramin_python.csv 파일에 저장했습니다.
2024-12-15 09:38:51,131 [INFO] 크롤링 완료. 다음 크롤링은 24시간 후.
```
