from flask import Blueprint, request, jsonify
import pymysql
from datetime import datetime
from db import get_db_connection  # get_db_connection 임포트

# Blueprint 생성
applications_bp = Blueprint('applications', __name__)

# 지원하기 API(완료)
'''
http://127.0.0.1:5000/applications

{
    "user_id": "test3",
    "job_id": 55
}
'''
@applications_bp.route('/applications', methods=['POST'])  # URL이 '/apply_'로 명확히 매핑됨
def apply_job():  # 함수 이름을 명확히 변경
    data = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # users 테이블에서 user_id 확인
            cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (data['user_id'],))
            user = cursor.fetchone()
            if not user:
                return jsonify({"error": "해당 user_id가 users 테이블에 존재하지 않습니다."}), 400
            
            # saramin_jobs 테이블에서 job_id 확인
            cursor.execute("SELECT id FROM saramin_jobs WHERE id = %s", (data['job_id'],))
            job = cursor.fetchone()
            if not job:
                return jsonify({"error": "해당 job_id가 saramin_jobs 테이블에 존재하지 않습니다."}), 400

            # apply_ 테이블에서 중복 확인
            cursor.execute(
                "SELECT id FROM apply_ WHERE user_id = %s AND job_id = %s",
                (data['user_id'], data['job_id'])
            )
            existing_application = cursor.fetchone()
            if existing_application:
                return jsonify({"message": "이미 해당 공고에 지원하셨습니다."}), 409

            # apply_ 테이블에 데이터 삽입
            sql = "INSERT INTO apply_ (user_id, job_id) VALUES (%s, %s)"
            cursor.execute(sql, (data['user_id'], data['job_id']))
            conn.commit()

        return jsonify({"message": "지원 등록 성공"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


        
# 지원 취소 API(완료)
'''
http://127.0.0.1:5000/applications/cancel

{
    "user_id": "test3",
    "job_id": 55
}
    
'''
@applications_bp.route('/applications/cancel', methods=['DELETE'])
def cancel_application():
    data = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 지원 내역이 있는지 확인
            sql_check = "SELECT id FROM apply_ WHERE user_id = %s AND job_id = %s"
            cursor.execute(sql_check, (data['user_id'], data['job_id']))
            record = cursor.fetchone()

            if not record:
                return jsonify({"error": "해당 지원 내역이 없습니다."}), 404
            
            # 지원 내역 삭제
            sql_delete = "DELETE FROM apply_ WHERE user_id = %s AND job_id = %s"
            cursor.execute(sql_delete, (data['user_id'], data['job_id']))
            conn.commit()
        
        return jsonify({"message": "지원 취소 성공"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# 지원 목록 조회 API(완료)
'''
http://127.0.0.1:5000/applications/list/test2

'''
@applications_bp.route('/applications/list/<string:user_id>', methods=['GET'])
def get_application_list(user_id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 지원 내역 조회
            sql = """
                SELECT a.id, a.job_id, j.title, j.company, j.location, a.created_at 
                FROM apply_ a
                JOIN saramin_jobs j ON a.job_id = j.id
                WHERE a.user_id = %s
            """
            cursor.execute(sql, (user_id,))
            applications = cursor.fetchall()
        
        if applications:
            return jsonify(applications), 200
        else:
            return jsonify({"message": "지원 내역이 없습니다."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()        
        