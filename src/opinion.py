from flasgger import swag_from
from flask import Blueprint, request, jsonify
import pymysql
from db import get_db_connection  # get_db_connection 임포트

opinion_bp = Blueprint('opinion', __name__)

# 사용자 의견 등록 API
'''
http://127.0.0.1:5000/opinion
{
    "user_id": "test2",
    "job_id": 101,
    "message": "이 회사의 워크 라이프 밸런스는 좋습니다."
}
'''
@opinion_bp.route('/opinion', methods=['POST'])
@swag_from({
    'tags': ['User Opinion(사용자 의견 관련 API)'],
    'summary': '사용자 의견 등록 API',
    'description': '특정 job_id에 대한 사용자의 의견을 등록합니다.',
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
                    'message': {'type': 'string', 'example': '이 회사의 워크 라이프 밸런스는 좋습니다.'}
                },
                'required': ['user_id', 'job_id', 'message']
            }
        }
    ],
    'responses': {
        201: {'description': '의견 등록 성공'},
        400: {'description': '유효하지 않은 user_id 또는 job_id'},
        500: {'description': '서버 에러'}
    }
})
def add_opinion():
    data = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE user_id = %s", (data['user_id'],))
            if not cursor.fetchone():
                return jsonify({"error": "해당 user_id가 존재하지 않습니다."}), 400

            cursor.execute("SELECT id FROM saramin_jobs WHERE id = %s", (data['job_id'],))
            if not cursor.fetchone():
                return jsonify({"error": "해당 job_id가 존재하지 않습니다."}), 400

            sql = "INSERT INTO _user_opinion (user_id, job_id, message) VALUES (%s, %s, %s)"
            cursor.execute(sql, (data['user_id'], data['job_id'], data['message']))
            conn.commit()

        return jsonify({"message": "의견 등록 성공"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# 사용자 의견 조회 API
'''
http://127.0.0.1:5000/opinion/101
'''
@opinion_bp.route('/opinion/<int:job_id>', methods=['GET'])
@swag_from({
    'tags': ['User Opinion(사용자 의견 관련 API)'],
    'summary': '사용자 의견 조회 API',
    'description': '특정 job_id에 대한 모든 사용자 의견을 조회합니다.',
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
        200: {'description': '의견 조회 성공'},
        404: {'description': '의견이 없는 경우'},
        500: {'description': '서버 에러'}
    }
})
def get_opinions(job_id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "SELECT user_id, message, created_at FROM _user_opinion WHERE job_id = %s"
            cursor.execute(sql, (job_id,))
            opinions = cursor.fetchall()

            if not opinions:
                return jsonify({"error": "해당 job_id에 대한 의견을 찾을 수 없습니다."}), 404

        return jsonify(opinions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# 사용자 의견 삭제 API
'''
http://127.0.0.1:5000/opinion/1
'''
@opinion_bp.route('/opinion/<int:id>', methods=['DELETE'])
@swag_from({
    'tags': ['User Opinion(사용자 의견 관련 API)'],
    'summary': '사용자 의견 삭제 API',
    'description': '사용자가 등록한 특정 의견을 삭제합니다.',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': '삭제할 의견 ID',
            'example': 1
        }
    ],
    'responses': {
        200: {'description': '의견 삭제 성공'},
        404: {'description': '의견을 찾을 수 없음'},
        500: {'description': '서버 에러'}
    }
})
def delete_opinion(id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "DELETE FROM _user_opinion WHERE id = %s"
            result = cursor.execute(sql, (id,))

            if result == 0:
                return jsonify({"error": "해당 의견을 찾을 수 없습니다."}), 404

            conn.commit()
        return jsonify({"message": "의견 삭제 성공"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
