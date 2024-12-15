from flask import Blueprint, request, jsonify
import pymysql
from datetime import datetime
from db import get_db_connection  # get_db_connection 임포트

# Blueprint 생성
jobs_bp = Blueprint('jobs', __name__)

# 채용 공고 조회 API(완료)
'''
http://127.0.0.1:5000/jobs
'''
@jobs_bp.route('/jobs', methods=['GET'])
def get_jobs():
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
