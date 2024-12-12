mysql -u root -p
mysql> select user, host from mysql.user;

o 권한 부여
https://goyunji.tistory.com/99

o 외부 접속 허용 user 생성 방법
mysql -u root -p
create user 'user1'@'%' identified by '1234';
exit
위와 같이 user 생성하고, 아래 내용 반영

https://i-kiin.net/?p=4600

출처: https://saii42.tistory.com/25 [saii 잡다한 블로그:티스토리]

////////////////////////////////////////////
o mysql root 비번 분실 대처

https://velog.io/@sonaky47/mysql-root-%ED%8C%A8%EC%8A%A4%EC%9B%8C%EB%93%9C-%EB%B6%84%EC%8B%A4%ED%96%88%EC%9D%84%EB%95%8C-ubuntu


///////////////////////////////////
*MySQL 서버 실행
///////////////////////////////////
sudo service mysql stop


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