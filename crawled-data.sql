/*
실행방법
  mysql -u root -p < ./crawled-data.sql
*/

-- MySQL 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS saramin_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

-- 권한 적용
FLUSH PRIVILEGES;

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

-- 지원 모델
CREATE TABLE IF NOT EXISTS apply_ (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    job_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES saramin_jobs(id) ON DELETE CASCADE
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

-- 사용자 추가 의견 테이블
CREATE TABLE IF NOT EXISTS _user_opinion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    job_id INT NOT NULL
