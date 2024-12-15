from flask import Blueprint, request, jsonify
import pymysql
from datetime import datetime
from db import get_db_connection  # get_db_connection 임포트

# Blueprint 생성
auth_bp = Blueprint('auth', __name__)

   
# 회원가입 API(완료)
'''
{
    "user_id": "test1",
    "email": "john.doe@example.com",
    "password": "111111",
    "name": "John Doe"
}
'''
@auth_bp.route('/auth/register', methods=['POST'])
def auth_register():
    data = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 비밀번호 암호화 및 DB 저장
            encoded_password = base64.b64encode(data['password'].encode()).decode()
            sql = "INSERT INTO users (user_id, email, password, name) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (data['user_id'], data['email'], encoded_password, data['name']))
            conn.commit()
        response = {"message": "회원가입 성공"}
    except Exception as e:
        response = {"error": str(e)}
    finally:
        conn.close()

    # ensure_ascii=False를 설정하여 한글을 제대로 출력
    return app.response_class(
        response=json.dumps(response, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )

# 로그인 API(완료)
{
    "user_id": "test4",
    "password": "111111"
}
@auth_bp.route('/auth/login', methods=['POST'])
def auth_login():
    data = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 사용자 ID 존재 여부 확인
            user_check_sql = "SELECT user_id FROM users WHERE user_id=%s"
            cursor.execute(user_check_sql, (data['user_id'],))
            user_exists = cursor.fetchone()

            if not user_exists:
                return jsonify({"error": "해당 user_id가 존재하지 않습니다."}), 404

            # 비밀번호를 Base64로 인코딩
            encoded_password = base64.b64encode(data['password'].encode()).decode()

            # 사용자 조회
            sql = "SELECT user_id, email, name, created_at FROM users WHERE user_id=%s AND password=%s"
            cursor.execute(sql, (data['user_id'], encoded_password))
            user = cursor.fetchone()

            if user:
                # `created_at` datetime을 문자열로 변환
                if 'created_at' in user and isinstance(user['created_at'], datetime):
                    user['created_at'] = user['created_at'].isoformat()

                return jsonify({"message": "로그인 성공", "user": user}), 200
            else:
                # 로그 남기기: 로그인 실패 로그 저장
                log_sql = "INSERT INTO logs (user_id, log_message) VALUES (%s, %s)"
                cursor.execute(log_sql, (data['user_id'], "로그인 실패"))
                conn.commit()

                return jsonify({"message": "로그인 실패"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

    # ensure_ascii=False 설정으로 한글을 제대로 출력
    return app.response_class(
        response=json.dumps(response, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )


# 회원 정보 조회 API(완료)
'''
http://127.0.0.1:5000/auth/profile/test1
http://127.0.0.1:5000/auth/profile/test2
http://127.0.0.1:5000/auth/profile/test3
http://127.0.0.1:5000/auth/profile/test4

'''
@auth_bp.route('/auth/profile/<string:user_id>', methods=['GET'])
def auth_user(user_id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "SELECT user_id, email, name, created_at FROM users WHERE user_id=%s"
            cursor.execute(sql, (user_id,))
            user = cursor.fetchone()
        if user:
            return jsonify(user), 200
        else:
            return jsonify({"message": "사용자를 찾을 수 없습니다."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
        
    # ensure_ascii=False를 설정하여 한글을 제대로 출력
    return app.response_class(
        response=json.dumps(response, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )
    
# 회원 정보 수정 API(완료)
'''
http://127.0.0.1:5000/auth/profile/test4

{
    "email": "new_email@example.com",
    "name": "Dr.Kim"
}
'''
@auth_bp.route('/autu/profile/<string:user_id>', methods=['PUT'])
def autu_update_user(user_id):
    print(f"Endpoint hit: /users/{user_id} with method PUT")
    print(f"Request JSON: {request.json}")
    data = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "UPDATE users SET email=%s, name=%s WHERE user_id=%s"
            cursor.execute(sql, (data.get('email'), data.get('name'), user_id))
            conn.commit()
        return jsonify({"message": "회원 정보 수정 성공"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

    # ensure_ascii=False를 설정하여 한글을 제대로 출력
    return app.response_class(
        response=json.dumps(response, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )        

'''
http://127.0.0.1:5000/auth/profile/change_password/test4

{
    "current_password": "111111",
    "new_password": "222222"
}

'''
# 회원 비밀 번호 변경 API(완료)
@auth_bp.route('/auth/profile/change_password/<string:user_id>', methods=['PUT'])
def change_password(user_id):
    """
    비밀번호 변경 API
    """
    data = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 기존 비밀번호 확인
            sql_check_password = "SELECT password FROM users WHERE user_id = %s"
            cursor.execute(sql_check_password, (user_id,))
            user = cursor.fetchone()

            if not user:
                return jsonify({"error": "해당 user_id가 존재하지 않습니다."}), 404

            # 입력된 현재 비밀번호 Base64 인코딩
            current_password_encoded = base64.b64encode(data['current_password'].encode()).decode()

            # 기존 비밀번호가 일치하는지 확인
            if user['password'] != current_password_encoded:
                return jsonify({"error": "현재 비밀번호가 일치하지 않습니다."}), 400

            # 새 비밀번호를 Base64로 인코딩 후 업데이트
            new_password_encoded = base64.b64encode(data['new_password'].encode()).decode()
            sql_update_password = "UPDATE users SET password=%s WHERE user_id=%s"
            cursor.execute(sql_update_password, (new_password_encoded, user_id))
            conn.commit()

        return jsonify({"message": "비밀번호 변경 성공"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


# 회원 탈퇴 API(완료)
@auth_bp.route('/autu/profile/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "DELETE FROM users WHERE user_id=%s"
            cursor.execute(sql, (user_id,))
            conn.commit()
        return jsonify({"message": "회원 탈퇴 성공"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
        
    # ensure_ascii=False를 설정하여 한글을 제대로 출력
    return app.response_class(
        response=json.dumps(response, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )             