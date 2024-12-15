/*
실행방법
  mysql -u root -p < ./crawled-data.sql
*/

-- MySQL 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS saramin_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

/*
-- 사용자 생성 및 권한 부여
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '555555';
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '555555';

CREATE USER IF NOT EXISTS 'flask_user'@'localhost' IDENTIFIED BY '555555';
ALTER USER 'flask_user'@'localhost' IDENTIFIED WITH mysql_native_password BY '555555';
GRANT ALL PRIVILEGES ON saramin_db.* TO 'flask_user'@'localhost';

CREATE USER IF NOT EXISTS 'flask_user'@'%' IDENTIFIED BY '555555';
ALTER USER 'flask_user'@'%' IDENTIFIED WITH mysql_native_password BY '555555';
GRANT ALL PRIVILEGES ON saramin_db.* TO 'flask_user'@'%';
*/

-- 권한 적용
FLUSH PRIVILEGES;

-- 출력: 데이터베이스 목록
SELECT '========== DATABASES LIST ==========' AS Section;
SHOW DATABASES;

-- 출력: MySQL 사용자 목록
SELECT '========== MYSQL USERS ==========' AS Section;
SELECT user, host FROM mysql.user;

-- saramin_db 데이터베이스 사용
USE saramin_db;

-- saramin_db 테이블 생성 모델
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,        
    user_id VARCHAR(255) NOT NULL UNIQUE,     
    email VARCHAR(255) NOT NULL UNIQUE,       
    password VARCHAR(255) NOT NULL,           
    name VARCHAR(255) NOT NULL,               
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 사람인 직업 모델
CREATE TABLE IF NOT EXISTS saramin_jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,        
    company VARCHAR(255) NOT NULL,            
    title VARCHAR(255) NOT NULL,              
    link TEXT NOT NULL,                           
    location VARCHAR(255) DEFAULT NULL,       
    experience VARCHAR(100) DEFAULT NULL,         
    education VARCHAR(100) DEFAULT NULL,      
    employment_type VARCHAR(100) DEFAULT NULL,    
    description TEXT DEFAULT NULL,                
    deadline DATE DEFAULT NULL,                   
    salary VARCHAR(100) DEFAULT NULL,             
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 사용자 공고문 북마크 모델
CREATE TABLE IF NOT EXISTS bookmarks (
    id INT AUTO_INCREMENT PRIMARY KEY,             
    user_id VARCHAR(255) NOT NULL,                 
    job_id INT NOT NULL,                           
    applied BOOLEAN DEFAULT FALSE,                 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES saramin_jobs(id) ON DELETE CASCADE
);

-- 사용자 행위 로그 모델
CREATE TABLE IF NOT EXISTS logs (
    id INT AUTO_INCREMENT PRIMARY KEY,        
    user_id VARCHAR(255) NOT NULL,            
    log_message TEXT NOT NULL,                
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 이력서(간단) 모델
CREATE TABLE IF NOT EXISTS _resume (
    id INT AUTO_INCREMENT PRIMARY KEY,        
    user_id VARCHAR(255) NOT NULL,            
    _resume_ TEXT NOT NULL,                
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 리뷰 모델
CREATE TABLE IF NOT EXISTS _review (
    id INT AUTO_INCREMENT PRIMARY KEY,             
    user_id VARCHAR(255) NOT NULL,                 
    job_id INT NOT NULL,                           
    review_score INT NOT NULL, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES saramin_jobs(id) ON DELETE CASCADE
);

-- 리크루터 모델
CREATE TABLE IF NOT EXISTS recruiter (
    id INT AUTO_INCREMENT PRIMARY KEY,        
    user_id VARCHAR(255) NOT NULL UNIQUE,     
    email VARCHAR(255) NOT NULL UNIQUE,       
    password VARCHAR(255) NOT NULL,           
    name VARCHAR(255) NOT NULL,               
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 알림 모델
CREATE TABLE IF NOT EXISTS user_notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,              
    recruiter_id VARCHAR(255) NOT NULL UNIQUE,      
    user_id VARCHAR(255) NOT NULL UNIQUE,           
    message TEXT NOT NULL,                          
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,  
    FOREIGN KEY (recruiter_id) REFERENCES recruiter(user_id), 
    FOREIGN KEY (user_id) REFERENCES users(user_id) 
);

-- 출력: saramin_db 테이블 목록
SELECT CONCAT('========== TABLES IN saramin_db ==========') AS Output;
SHOW TABLES;

-- 출력: users 테이블 구조
SELECT '========== STRUCTURE OF users TABLE ==========' AS Section;
DESCRIBE users;

-- 출력: saramin_jobs 테이블 구조
SELECT '========== STRUCTURE OF saramin_jobs TABLE ==========' AS Section;
DESCRIBE saramin_jobs;

-- 출력: bookmarks 테이블 구조
SELECT '========== STRUCTURE OF bookmarks TABLE ==========' AS Section;
DESCRIBE bookmarks;

-- 출력: logs 테이블 구조
SELECT '========== STRUCTURE OF logs TABLE ==========' AS Section;
DESCRIBE logs;
