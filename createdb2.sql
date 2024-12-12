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

-- users 테이블 생성 (회원 정보)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
/*
-- saramin_jobs 테이블 생성 (채용 공고 정보)
CREATE TABLE IF NOT EXISTS saramin_jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    salary VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
*/

-- 채용 공고 테이블 생성
CREATE TABLE IF NOT EXISTS saramin_jobs (
    id INT AUTO_INCREMENT PRIMARY KEY, -- 고유 ID
    company VARCHAR(255) NOT NULL, -- 회사명
    title VARCHAR(255) NOT NULL, -- 공고 제목
    location VARCHAR(255) DEFAULT NULL, -- 근무 지역
    salary VARCHAR(100) DEFAULT NULL, -- 연봉 정보
    link TEXT NOT NULL, -- 공고 링크
    education VARCHAR(100) DEFAULT NULL, -- 학력 요구사항
    description TEXT DEFAULT NULL, -- 공고 설명
    employment_type VARCHAR(100) DEFAULT NULL, -- 고용 형태
    experience VARCHAR(100) DEFAULT NULL, -- 경력 요구사항
    deadline DATE DEFAULT NULL, -- 마감일
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- 데이터 생성 시간
); -- ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- favorites 테이블 생성 (사용자의 관심 채용 공고)
CREATE TABLE IF NOT EXISTS favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    job_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES saramin_jobs(id) ON DELETE CASCADE
);

-- 데이터 확인
-- SHOW TABLES;

-- 테이블 구조 확인
---DESCRIBE saramin_jobs;
