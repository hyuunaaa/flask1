from flasgger import Swagger, swag_from
from flask import Blueprint, request, jsonify
import pymysql
from db import get_db_connection  # get_db_connection 임포트

# Blueprint 생성
review_bp = Blueprint('review', __name__)

# 리뷰 등록 API
'''
http://127.0.0.1:5000/review
{
    "user_id": "test2",
    "job_id": 101,
    "review_score": 5
}
'''
@review_bp.route('/review', methods=['POST'])
@swag_from({
    'tags': ['Review(채용 공고 리뷰 관련 API)'],
    'summary': '리뷰 등록 API',
    'description': '특정 job_id에 대해 사용자가 별점을 등록합니다.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'user_id': {'type': 'string', 'example': 'test2'},
                    'job_id': {'type': 'integer', 'example': 101},
                    'review_score': {'type': 'integer', 'example': 5}
                },
                'required': ['user_id', 'job_id', 'review_score']
            }
        }
    ],
    'responses': {
        201: {
            'description': '리뷰 등록 성공',
            'examples': {
                'application/json': {'message': '리뷰 등록 성공'}
            }
        },
        400: {
            'description': '유효하지 않은 user_id 또는 job_id',
            'examples': {
                'application/json': {'error': '해당 user_id 또는 job_id가 존재하지 않습니다.'}
            }
        },
        500: {
            'description': '서버 에러',
            'examples': {
                'application/json': {'error': '서버 에러 메시지'}
            }
        }
    }
})
def add_review():
    data = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # user_id가 users 테이블에 존재하는지 확인
            cursor.execute("SELECT id FROM users WHERE user_id = %s", (data['user_id'],))
            user = cursor.fetchone()
            if not user:
                return jsonify({"error": "해당 user_id가 존재하지 않습니다."}), 400
            
            # job_id가 saramin_jobs 테이블에 존재하는지 확인
            cursor.execute("SELECT id FROM saramin_jobs WHERE id = %s", (data['job_id'],))
            job = cursor.fetchone()
            if not job:
                return jsonify({"error": "해당 job_id가 존재하지 않습니다."}), 400
            
            # 리뷰 테이블에 삽입
            sql = "INSERT INTO _review (user_id, job_id, review_score) VALUES (%s, %s, %s)"
            cursor.execute(sql, (data['user_id'], data['job_id'], data['review_score']))
            conn.commit()

        return jsonify({"message": "리뷰 등록 성공"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# 특정 job_id에 대한 리뷰 조회 API
'''
http://127.0.0.1:5000/review/101
'''
@review_bp.route('/review/<int:job_id>', methods=['GET'])
@swag_from({
    'tags': ['Review(채용 공고 리뷰 관련 API)'],
    'summary': '리뷰 조회 API',
    'description': '특정 job_id에 대한 모든 리뷰를 조회합니다.',
    'parameters': [
        {
            'name': 'job_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': '조회할 job_id',
            'example': 101
        }
    ],
    'responses': {
        200: {
            'description': '리뷰 조회 성공',
            'examples': {
                'application/json': [
                    {"user_id": "test2", "job_id": 101, "review_score": 5, "created_at": "2024-12-15T10:00:00"}
                ]
            }
        },
        404: {
            'description': '리뷰가 없는 경우',
            'examples': {
                'application/json': {'error': '해당 job_id에 대한 리뷰를 찾을 수 없습니다.'}
            }
        },
        500: {
            'description': '서버 에러',
            'examples': {
                'application/json': {'error': '서버 에러 메시지'}
            }
        }
    }
})
def get_reviews(job_id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 특정 job_id에 대한 모든 리뷰 조회
            sql = """
                SELECT user_id, job_id, review_score, created_at
                FROM _review
                WHERE job_id = %s
            """
            cursor.execute(sql, (job_id,))
            reviews = cursor.fetchall()

            if not reviews:
                return jsonify({"error": "해당 job_id에 대한 리뷰를 찾을 수 없습니다."}), 404

        return jsonify(reviews), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
