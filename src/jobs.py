from flask import Blueprint, request, jsonify
import pymysql
from datetime import datetime
from db import get_db_connection  # get_db_connection 임포트

# Blueprint 생성
jobs_bp = Blueprint('jobs', __name__)

# 채용 공고 조회 API(완료)
'''
http://127.0.0.1:8080/jobs
http://113.198.66.75:10018/jobs
'''
@jobs_bp.route('/jobs', methods=['GET'])
def get_jobs():
    """
    채용 공고 목록 조회 API
    ---
    tags:
      - Job Posting(채용공고 관련 API)
    responses:
      200:
        description: 채용 공고 목록 조회 성공
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: "채용 공고 ID"
              company:
                type: string
                description: "회사 이름"
              title:
                type: string
                description: "공고 제목"
              location:
                type: string
                description: "근무 지역"
              salary:
                type: string
                description: "연봉"
              description:
                type: string
                description: "공고 설명"
        examples:
          application/json: |
            [
              {
                "id": 1,
                "company": "ABC Corp",
                "title": "Software Engineer",
                "location": "Seoul",
                "salary": "50M KRW",
                "description": "Job description here"
              },
              {
                "id": 2,
                "company": "XYZ Inc",
                "title": "Data Scientist",
                "location": "Busan",
                "salary": "55M KRW",
                "description": "Another job description here"
              }
            ]
      500:
        description: 서버 오류
        schema:
          type: object
          properties:
            error:
              type: string
              """
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM saramin_jobs")
            jobs = cursor.fetchall()
        return jsonify(jobs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# 채용 공고 상세 조회 API(완료)
@jobs_bp.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """
    채용 공고 상세 조회 API
    ---
    tags:
      - Job Posting(채용공고 관련 API)
    parameters:
      - name: job_id
        in: path
        required: true
        type: integer
        description: 상세 조회할 채용 공고 ID
    responses:
      200:
        description: 채용 공고 상세 조회 성공
        schema:
          type: object
          properties:
            id:
              type: integer
            company:
              type: string
            title:
              type: string
            location:
              type: string
            salary:
              type: string
            description:
              type: string
        examples:
          application/json: |
            {
              "id": 1,
              "company": "ABC Corp",
              "title": "Software Engineer",
              "location": "Seoul",
              "salary": "50M KRW",
              "description": "Job description here"
            }
      404:
        description: 공고를 찾을 수 없음
        schema:
          type: object
          properties:
            message:
              type: string
        examples:
          application/json: |
            {
              "message": "채용 공고를 찾을 수 없습니다."
            }
      500:
        description: 서버 오류
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "SELECT * FROM saramin_jobs WHERE id=%s"
            cursor.execute(sql, (job_id,))
            job = cursor.fetchone()
        if job:
            return jsonify(job), 200
        else:
            return jsonify({"message": "채용 공고를 찾을 수 없습니다."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# 채용 공고 등록 API(완료)
'''
http://127.0.0.1:5000/jobs

{
    "company": "1111",
    "description": "설명",
    "location": "지역",
    "salary": "연봉",
    "title": "타이틀"
}
'''
@jobs_bp.route('/jobs', methods=['POST'])
def add_job():
    """
    채용 공고 등록 API
    ---
    tags:
      - Job Posting(채용공고 관련 API)
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            company:
              type: string
              description: "회사 이름"
              example: "ABC Corp"
            title:
              type: string
              description: "공고 제목"
              example: "Software Engineer"
            location:
              type: string
              description: "근무 지역"
              example: "Seoul"
            salary:
              type: string
              description: "연봉"
              example: "50M KRW"
            description:
              type: string
              description: "공고 설명"
              example: "Job description here"
    responses:
      201:
        description: 공고 등록 성공
        schema:
          type: object
          properties:
            message:
              type: string
        examples:
          application/json: |
            {
              "message": "채용 공고 등록 성공"
            }
      500:
        description: 서버 오류
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO saramin_jobs (company, title, location, salary, description)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                data.get('company'), data.get('title'), 
                data.get('location'), data.get('salary'), data.get('description')                
            ))
            conn.commit()
        return jsonify({"message": "채용 공고 등록 성공"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# 채용 공고 수정 API(완료)
'''
http://127.0.0.1:5000/jobs/121

{
    "company": "1111222",
    "description": "설명",
    "location": "지역",
    "salary": "연봉",
    "title": "타이틀"
}
'''
@jobs_bp.route('/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    """
    채용 공고 수정 API
    ---
    tags:
      - Job Posting(채용공고 관련 API)
    parameters:
      - name: job_id
        in: path
        required: true
        type: integer
        description: 수정할 채용 공고 ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            company:
              type: string
              description: "회사 이름"
            title:
              type: string
              description: "공고 제목"
            location:
              type: string
              description: "근무 지역"
            salary:
              type: string
              description: "연봉"
            description:
              type: string
              description: "공고 설명"
    responses:
      200:
        description: 공고 수정 성공
        schema:
          type: object
          properties:
            message:
              type: string
        examples:
          application/json: |
            {
              "message": "채용 공고 수정 성공"
            }
      500:
        description: 서버 오류
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
            UPDATE saramin_jobs 
            SET title=%s, company=%s, location=%s, salary=%s, description=%s
            WHERE id=%s
            """
            cursor.execute(sql, (
                data.get('title'), data.get('company'), data.get('location'), 
                data.get('salary'), data.get('description'), job_id
            ))
            conn.commit()
        return jsonify({"message": "채용 공고 수정 성공"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# 채용 공고 삭제 API(완료)
'''
http://127.0.0.1:5000/jobs/122
'''
@jobs_bp.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    """
    채용 공고 삭제 API
    ---
    tags:
      - Job Posting(채용공고 관련 API)
    parameters:
      - name: job_id
        in: path
        required: true
        type: integer
        description: 삭제할 채용 공고 ID
    responses:
      200:
        description: 공고 삭제 성공
        schema:
          type: object
          properties:
            message:
              type: string
        examples:
          application/json: |
            {
              "message": "채용 공고 삭제 성공"
            }
      500:
        description: 서버 오류
        schema:
          type: object
          properties:
            error:
              type: string
    """

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "DELETE FROM saramin_jobs WHERE id=%s"
            cursor.execute(sql, (job_id,))
            conn.commit()
        return jsonify({"message": "채용 공고 삭제 성공"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
