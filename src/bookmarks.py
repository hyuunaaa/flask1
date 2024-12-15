from flask import Blueprint, request, jsonify
import pymysql
from datetime import datetime
from db import get_db_connection  # get_db_connection 임포트

# Blueprint 생성
bookmarks_bp = Blueprint('bookmarks', __name__)
    
# 관심 등록 API(완료)
'''
http://127.0.0.1:5000/bookmarks
{
    "user_id": "test2",
    "job_id": 10,
    "applied": false
}

'''
@bookmarks_bp.route('/bookmarks', methods=['POST'])
def add_favorite():
    data = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # user_id가 users 테이블에 존재하는지 확인
            cursor.execute("SELECT id FROM users WHERE user_id = %s", (data['user_id'],))
            user = cursor.fetchone()
            if not user:
                return jsonify({"error": "해당 user_id가 users 테이블에 존재하지 않습니다."}), 400
            
            # job_id가 saramin_jobs 테이블에 존재하는지 확인
            cursor.execute("SELECT id FROM saramin_jobs WHERE id = %s", (data['job_id'],))
            job = cursor.fetchone()
            if not job:
                return jsonify({"error": "해당 job_id가 saramin_jobs 테이블에 존재하지 않습니다."}), 400

            # bookmarks 테이블에 삽입
            sql = "INSERT INTO bookmarks (user_id, job_id) VALUES (%s, %s)"
            cursor.execute(sql, (data['user_id'], data['job_id']))
            conn.commit()

        return jsonify({"message": "관심 등록 성공"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# 사용자 관심 공고 조회 API(완료)
'''
http://127.0.0.1:5000/bookmarks/test3
'''
@bookmarks_bp.route('/bookmarks/<string:user_id>', methods=['GET'])
def get_user_favorites(user_id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
            SELECT saramin_jobs.* 
            FROM bookmarks
            JOIN saramin_jobs ON bookmarks.job_id = saramin_jobs.id
            WHERE bookmarks.user_id = %s
            """
            cursor.execute(sql, (user_id,))
            bookmarks = cursor.fetchall()
        return jsonify(bookmarks), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()