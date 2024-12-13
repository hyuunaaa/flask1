-- MySQL 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS saramin_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

-- flask_user 사용자 생성 및 권한 부여
CREATE USER IF NOT EXISTS 'flask_user'@'localhost' IDENTIFIED BY '555555';
GRANT ALL PRIVILEGES ON saramin_db.* TO 'flask_user'@'localhost';

-- 외부 접속을 위한 사용자 생성 및 권한 부여
CREATE USER IF NOT EXISTS 'flask_user'@'%' IDENTIFIED BY '555555';
GRANT ALL PRIVILEGES ON saramin_db.* TO 'flask_user'@'%';

-- 권한 적용
FLUSH PRIVILEGES;

-- saramin_db 데이터베이스 사용
USE saramin_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,         -- 자동 증가 ID
    user_id VARCHAR(255) NOT NULL UNIQUE,      -- 필수, 유일한 사용자 ID
    email VARCHAR(255) NOT NULL UNIQUE,        -- 필수, 유일한 이메일
    password VARCHAR(255) NOT NULL,            -- 필수 비밀번호
    name VARCHAR(255) NOT NULL,                -- 필수 사용자 이름
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- 생성 시간
);
-- 채용 공고 테이블 생성
CREATE TABLE IF NOT EXISTS saramin_jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,        -- 고유 ID
    company VARCHAR(255) NOT NULL,            -- 회사명
    title VARCHAR(255) NOT NULL,              -- 공고 제목
    location VARCHAR(255) DEFAULT NULL,       -- 근무 지역
    salary VARCHAR(100) DEFAULT NULL,         -- 연봉 정보
    link TEXT NOT NULL,                       -- 공고 링크
    education VARCHAR(100) DEFAULT NULL,      -- 학력 요구사항
    description TEXT DEFAULT NULL,            -- 공고 설명
    employment_type VARCHAR(100) DEFAULT NULL, -- 고용 형태
    experience VARCHAR(100) DEFAULT NULL,     -- 경력 요구사항
    deadline DATE DEFAULT NULL,               -- 마감일
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 데이터 생성 시간
);

-- favorites 테이블 생성 (사용자의 관심 채용 공고)
CREATE TABLE IF NOT EXISTS favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,             -- 고유 ID
    user_id VARCHAR(255) NOT NULL,                 -- users 테이블의 user_id를 참조 (VARCHAR로 수정)
    job_id INT NOT NULL,                           -- saramin_jobs 테이블의 id를 참조
    applied BOOLEAN DEFAULT FALSE,                 -- 지원 여부 (기본값: FALSE)    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 생성 시간
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE, -- 참조 무결성 (users 테이블의 user_id와 연결)
    FOREIGN KEY (job_id) REFERENCES saramin_jobs(id) ON DELETE CASCADE -- 참조 무결성
);

CREATE TABLE IF NOT EXISTS apply_ (
    id INT AUTO_INCREMENT PRIMARY KEY,             -- 고유 ID
    user_id VARCHAR(255) NOT NULL,                 -- users 테이블의 user_id를 참조 (VARCHAR로 수정)
    job_id INT NOT NULL,                           -- saramin_jobs 테이블의 id를 참조
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 생성 시간
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE, -- 참조 무결성 (users 테이블의 user_id와 연결)
    FOREIGN KEY (job_id) REFERENCES saramin_jobs(id) ON DELETE CASCADE -- 참조 무결성
);

CREATE TABLE IF NOT EXISTS apply_ (
    id INT AUTO_INCREMENT PRIMARY KEY,             -- 고유 ID
    user_id VARCHAR(255) NOT NULL,                 -- users 테이블의 user_id를 참조 (VARCHAR로 수정)
    log_error VARCHAR(255) NOT NULL,                 -- users 테이블의 user_id를 참조 (VARCHAR로 수정)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 생성 시간
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE, -- 참조 무결성 (users 테이블의 user_id와 연결)
    FOREIGN KEY (job_id) REFERENCES saramin_jobs(id) ON DELETE CASCADE -- 참조 무결성
);

CREATE TABLE IF NOT EXISTS logs (
    id INT AUTO_INCREMENT PRIMARY KEY,        -- 고유 ID
    user_id VARCHAR(255) NOT NULL,            -- 로그를 생성한 사용자 ID
    log_message TEXT NOT NULL,                -- 로그 내용
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 로그 생성 시간
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE -- users 테이블의 user_id와 연결
);

-- DROP TABLE IF EXISTS favorites;
/*
CREATE TABLE IF NOT EXISTS favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,             -- 고유 ID
    user_id INT NOT NULL,                          -- users 테이블의 id를 참조
    job_id INT NOT NULL,                           -- saramin_jobs 테이블의 id를 참조
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 생성 시간
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE, -- 참조 무결성
    FOREIGN KEY (job_id) REFERENCES saramin_jobs(id) ON DELETE CASCADE -- 참조 무결성
);
*/

-- 데이터 확인
-- SHOW TABLES;

-- 테이블 구조 확인
---DESCRIBE saramin_jobs;
