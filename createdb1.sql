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

-- favorites 테이블 생성 (사용자의 관심 채용 공고)
CREATE TABLE IF NOT EXISTS favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    job_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES saramin_jobs(id) ON DELETE CASCADE
);
