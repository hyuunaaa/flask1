from flasgger import Swagger, swag_from
from flask import Blueprint, request, jsonify
import pymysql
from db import get_db_connection  # get_db_connection 임포트

# Blueprint 생성
resume_bp = Blueprint('resume', __name__)

# 이력서 등록 API
'''
http://127.0.0.1:5000/resume
{
    "user_id": "test2",
    "_resume_": "안녕하세요, 제 이력서입니다"
}
'''
@resume_bp.route('/resume', methods=['POST'])
@swag_from({
    'tags': ['Resume(이력서 관련 API)'],
    'summary': '이력서 등록 API',
    'description': '사용자의 이력서를 등록합니다.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'user_id': {'type': 'string', 'example': 'test2'},
                    '_resume_': {'type': 'string', 'example': '안녕하세요, 제 이력서입니다'}
                },
                'required': ['user_id', '_resume_']
            }
        }
    ],
    'responses': {
        201: {
            'description': '이력서 등록 성공',
            'examples': {
                'application/json': {'message': '이력서 등록 성공'}
            }
        },
        400: {
            'description': '유효하지 않은 user_id',
            'examples': {
                'application/json': {'error': '해당 user_id가 users 테이블에 존재하지 않습니다.'}
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
def add_resume():
    data = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # user_id가 users 테이블에 존재하는지 확인
            cursor.execute("SELECT id FROM users WHERE user_id = %s", (data['user_id'],))
            user = cursor.fetchone()
            if not user:
                return jsonify({"error": "해당 user_id가 users 테이블에 존재하지 않습니다."}), 400
            
            # resume 테이블에 삽입
            sql = "INSERT INTO _resume (user_id, _resume_) VALUES (%s, %s)"
            cursor.execute(sql, (data['user_id'], data['_resume_']))
            conn.commit()

        return jsonify({"message": "이력서 등록 성공"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


# 이력서 조회 API
'''
http://127.0.0.1:5000/resume/test2
'''
@resume_bp.route('/resume/<string:user_id>', methods=['GET'])
@swag_from({
    'tags': ['Resume(이력서 관련 API)'],
    'summary': '이력서 조회 API',
    'description': '특정 user_id에 대한 이력서를 조회합니다.',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': '조회할 사용자의 ID',
            'example': 'test2'
        }
    ],
    'responses': {
        200: {
            'description': '이력서 조회 성공',
            'examples': {
                'application/json': {'user_id': 'test2', '_resume_': '안녕하세요, 제 이력서입니다'}
            }
        },
        404: {
            'description': '이력서가 없는 경우',
            'examples': {
                'application/json': {'error': '해당 user_id에 대한 이력서를 찾을 수 없습니다.'}
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
def get_user_resume(user_id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 특정 user_id의 이력서 조회
            sql = """
                SELECT user_id, _resume_
                FROM _resume
                WHERE user_id = %s
            """
            cursor.execute(sql, (user_id,))
            resume = cursor.fetchone()  # 한 개의 결과만 가져오기

            if not resume:
                return jsonify({"error": "해당 user_id에 대한 이력서를 찾을 수 없습니다."}), 404

        return jsonify(resume), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
