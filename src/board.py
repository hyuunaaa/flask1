from flasgger import swag_from
from flask import Blueprint, request, jsonify
import pymysql
from db import get_db_connection

board_bp = Blueprint('board', __name__)

# 게시글 등록 API
'''
http://127.0.0.1:5000/board
{
    "user_id": "test2",
    "board": "게시판에 글을 남깁니다."
}
'''
@board_bp.route('/board', methods=['POST'])
@swag_from({
    'tags': ['User Board(게시판 관련 API)'],
    'summary': '게시글 등록 API',
    'description': '사용자가 게시판에 글을 등록합니다.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'user_id': {'type': 'string', 'example': 'test2'},
                    'board': {'type': 'string', 'example': '게시판에 글을 남깁니다.'}
                },
                'required': ['user_id', 'board']
            }
        }
    ],
    'responses': {
        201: {'description': '게시글 등록 성공'},
        400: {'description': '유효하지 않은 user_id'},
        500: {'description': '서버 에러'}
    }
})
def add_board():
    data = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE user_id = %s", (data['user_id'],))
            if not cursor.fetchone():
                return jsonify({"error": "해당 user_id가 존재하지 않습니다."}), 400

            sql = "INSERT INTO _user_board (user_id, board) VALUES (%s, %s)"
            cursor.execute(sql, (data['user_id'], data['board']))
            conn.commit()

        return jsonify({"message": "게시글 등록 성공"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# 게시글 조회 API
'''
http://127.0.0.1:5000/board
'''
@board_bp.route('/board', methods=['GET'])
@swag_from({
    'tags': ['User Board(게시판 관련 API)'],
    'summary': '게시글 조회 API',
    'description': '모든 게시글을 조회합니다.',
    'responses': {
        200: {'description': '게시글 조회 성공'},
        500: {'description': '서버 에러'}
    }
})
def get_board():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "SELECT user_id, board, created_at FROM _user_board"
            cursor.execute(sql)
            boards = cursor.fetchall()

        return jsonify(boards), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# 게시글 삭제 API
'''
http://127.0.0.1:5000/board/1
'''
@board_bp.route('/board/<int:id>', methods=['DELETE'])
@swag_from({
    'tags': ['User Board(게시판 관련 API)'],
    'summary': '게시글 삭제 API',
    'description': '특정 게시글을 삭제합니다.',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': '삭제할 게시글 ID',
            'example': 1
        }
    ],
    'responses': {
        200: {'description': '게시글 삭제 성공'},
        404: {'description': '게시글을 찾을 수 없음'},
        500: {'description': '서버 에러'}
    }
})
def delete_board(id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "DELETE FROM _user_board WHERE id = %s"
            result = cursor.execute(sql, (id,))

            if result == 0:
                return jsonify({"error": "해당 게시글을 찾을 수 없습니다."}), 404

            conn.commit()
        return jsonify({"message": "게시글 삭제 성공"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
