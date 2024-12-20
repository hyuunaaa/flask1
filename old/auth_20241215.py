import jwt  # JWT 토큰 생성 및 검증을 위한 라이브러리
from flask import Blueprint, request, jsonify
import pymysql
from datetime import datetime, timedelta  # timedelta 추가
from db import get_db_connection  # get_db_connection 임포트
import bcrypt

# Flask Blueprint 설정
auth_bp = Blueprint('auth', __name__)

# JWT Secret Key
SECRET_KEY = 'your_secret_key'

# DB 연결 설정
db_config = {
    "host": "localhost",
    "user": "flask_user",
    "password": "555555",
    "database": "saramin_db",
    "charset": "utf8mb4"
}

# DB 연결 함수
def get_db_connection():
    return pymysql.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        cursorclass=pymysql.cursors.DictCursor
    )

# JWT 토큰 생성 함수
def create_jwt_token(user_id):
    """
    JWT 토큰 생성
    """
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=1),  # 1시간 유효
        'iat': datetime.utcnow()  # 토큰 발급 시간
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# 토큰 검증 미들웨어
def token_required(f):
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "토큰이 제공되지 않았습니다."}), 401

        try:
            # JWT 검증
            decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user_id = decoded['user_id']  # 요청 객체에 user_id 추가
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "토큰이 만료되었습니다."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "유효하지 않은 토큰입니다."}), 401

        return f(*args, **kwargs)
    return decorated

# 비밀번호 암호화
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# 비밀번호 검증
def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# 회원가입
'''
http://127.0.0.1:5000//auth/register

{
    "user_id": "test1",
    "email": "test1@example.com",
    "password": "111111",
    "name": "name1"
}
'''
@auth_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 비밀번호 암호화
            hashed_password = hash_password(data['password'])

            sql = "INSERT INTO users (user_id, email, password, name) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (data['user_id'], data['email'], hashed_password, data['name']))
            conn.commit()

        return jsonify({"message": "회원가입 성공"}), 201
    except pymysql.MySQLError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# 로그인
'''
Req:
http://127.0.0.1:5000//auth/login

{
    "user_id": "test1",
    "password": "111111"
}

Res:
{
    "message": "로그인 성공",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoidGVzdDEiLCJleHAiOjE3MzQyNDUwMzksImlhdCI6MTczNDI0MTQzOX0.68WY79NYhyKgn6TQWDt9Ewu-_7dvVofEe2hWfrVNqZo"
}
'''
@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.json  # 요청 데이터
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # user_id를 기준으로 사용자를 조회
            sql = "SELECT user_id, password FROM users WHERE user_id = %s"
            cursor.execute(sql, (data['user_id'],))
            user = cursor.fetchone()

        # 사용자 존재 여부와 비밀번호 확인
        if not user or not check_password(data['password'], user['password']):
            return jsonify({"error": "user_id 또는 비밀번호가 잘못되었습니다."}), 401

        # JWT 토큰 발급
        token = create_jwt_token(user['user_id'])
        return jsonify({"message": "로그인 성공", "token": token}), 200
    except pymysql.MySQLError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


# 토큰 갱신
@auth_bp.route('/token/refresh', methods=['POST'])
@token_required
def refresh_token():
    try:
        # 기존 user_id를 기반으로 새로운 토큰 생성
        token = create_jwt_token(request.user_id)
        return jsonify({"message": "토큰 갱신 성공", "token": token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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