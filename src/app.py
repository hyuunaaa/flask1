import sys  # 명령행 인자를 읽기 위한 모듈
from flask import Flask, request, jsonify
import pymysql
import base64
import json
from datetime import datetime
from db import get_db_connection  # get_db_connection 임포트
from flasgger import Swagger
from dotenv import load_dotenv  # .env 파일 로드
import os  # 환경 변수 접근

from jobs import jobs_bp  # jobs.py에서 Blueprint 임포트
from auth import auth_bp  # auth.py에서 Blueprint 임포트
from bookmarks import bookmarks_bp  # bookmarks.py에서 Blueprint 임포트
from applications import applications_bp  # applications.py에서 Blueprint 임포트
from resume import resume_bp  # resume.py에서 Blueprint 임포트
from review import review_bp  # review.py에서 Blueprint 임포트
from opinion import opinion_bp  # opinion.py에서 Blueprint 임포트
from board import board_bp  # board.py에서 Blueprint 임포트

# .env 파일 로드
load_dotenv()

app = Flask(__name__)

# Swagger 설정
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "김현아의 JOB API",
        "description": "사람인 백엔드 서버 만들기",
        "version": "1.0.0"
    },
    # .env 파일에서 'SWAGGER_HOST' 값을 읽어 사용
    "host": os.getenv("SWAGGER_HOST", "localhost:5000"),  
    "basePath": "/",
    "schemes": ["http"]
}
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api-docs/"
}

Swagger(app, template=swagger_template, config=swagger_config)

# 기본 루트 경로
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Flask API is running!"}), 200

# Blueprint 등록
app.register_blueprint(jobs_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(bookmarks_bp)
app.register_blueprint(applications_bp)
app.register_blueprint(resume_bp)
app.register_blueprint(review_bp)
app.register_blueprint(opinion_bp)
app.register_blueprint(board_bp)

if __name__ == '__main__':
    # 명령행에서 포트 인자 읽기
    port = 8080  # 기본값 설정
    if len(sys.argv) > 1:  # 인자가 있을 경우
        try:
            port = int(sys.argv[1])  # 첫 번째 인자를 포트로 사용
        except ValueError:
            print("Invalid port provided. Using default port 8080.")

    app.run(host='0.0.0.0', port=port, debug=True)
