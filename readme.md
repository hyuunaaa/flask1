///////////////////////////////////
*MySQL 서버 실행
///////////////////////////////////
MySQL 서비스 시작:

sudo service mysql start
MySQL 서비스 상태 확인:

sudo service mysql status
active (running) 상태라면 MySQL 서버가 실행 중입니다.
MySQL 서버 재시작 (필요한 경우):

sudo service mysql restart
MySQL 서버 중지:

sudo service mysql stop


///////////////////////////////////
**db_create.sql 실행 
///////////////////////////////////
2. 명령줄에서 직접 실행
MySQL 명령어를 사용해 SQL 파일 실행:

mysql -u root -p < /path/to/db_create.sql
MySQL 서버가 파일 내의 명령어를 실행하고 설정을 완료합니다.
실행 결과 확인:

mysql -u root -p
USE saramin_db;
SHOW TABLES;
===================================
. MySQL 클라이언트에서 실행
단계 1: MySQL 서버 접속
MySQL 서버가 실행 중인지 확인:

sudo systemctl status mysql
MySQL 클라이언트 접속:

mysql -u root -p
root 계정 비밀번호를 입력하여 접속합니다.
단계 2: SQL 파일 실행
MySQL 셸에서 파일 실행:

SOURCE /path/to/db_create.sql;
/path/to/db_create.sql를 파일의 실제 경로로 바꿉니다.
실행 완료 후 테이블 확인:

SHOW DATABASES;
USE saramin_db;
SHOW TABLES;

//////////////////////////////////////////////////////
[] 파이썬 가상환경

python3 -m venv flask_env
가상환경 활성화:

pip install pymysql

source ../flask_env/bin/activate
가상환경 내에서 Flask 설치:

pip install flask
설치 확인:

python -m flask --version
가상환경 비활성화 (작업 완료 후):

deactivate