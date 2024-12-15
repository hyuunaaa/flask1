import jwt  # JWT 토큰 생성 및 검증을 위한 라이브러리
from flask import Blueprint, request, jsonify
import pymysql
from datetime import datetime, timedelta  # timedelta 추가
from db import get_db_connection  # get_db_connection 임포트
import bcrypt
from flasgger import swag_from

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
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1),  # 1시간 유효
        "iat": datetime.utcnow(),  # 토큰 발급 시간
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# 토큰 검증 미들웨어
def token_required(f):
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "토큰이 제공되지 않았습니다."}), 401

        try:
            # JWT 검증
            token = token.split(" ")[1]  # "Bearer <token>"에서 토큰 부분만 추출
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            g.user_id = decoded["user_id"]  # 글로벌 컨텍스트에 사용자 ID 추가
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "토큰이 만료되었습니다."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "유효하지 않은 토큰입니다."}), 401

        return f(*args, **kwargs)

    return decorated

# 비밀번호 암호화
def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

# 비밀번호 검증
def check_password(password, hashed):
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

# 회원가입
'''
http://127.0.0.1:5000/auth/register
http://113.198.66.75:10018/auth/register

Req:
{
    "user_id": "test1",
    "email": "test1@example.com",
    "password": "111111",
    "name": "name1"
}
Res:
{
    "message": "회원가입 성공"
}
'''
# 회원가입
@auth_bp.route("/auth/register", methods=["POST"])
def register():
    """
    회원가입 API
    ---
    tags:
      - "Authentication(회원가입/로그인 관련 API)"
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - user_id
            - email
            - password
            - name
          properties:
            user_id:
              type: string
              example: test_user
              description: 사용자 ID
            email:
              type: string
              example: test@example.com
              description: 사용자 이메일
            password:
              type: string
              example: password123
              description: 사용자 비밀번호
            name:
              type: string
              example: John Doe
              description: 사용자 이름
    responses:
      201:
        description: 회원가입 성공
        schema:
          type: object
          properties:
            message:
              type: string
              example: 회원가입 성공
      500:
        description: 데이터베이스 작업 중 에러 발생
        schema:
          type: object
          properties:
            error:
              type: string
              example: 데이터베이스 에러 메시지
    """    
    data = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 비밀번호 암호화
            hashed_password = hash_password(data["password"])
            sql = "INSERT INTO users (user_id, email, password, name) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (data["user_id"], data["email"], hashed_password, data["name"]))
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
@auth_bp.route("/auth/login", methods=["POST"])
#@swag_from('docs/auth.yml')
def login():
    """
    로그인 API
    ---
    tags:
      - "Authentication(회원가입/로그인 관련 API)"
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - user_id
            - password
          properties:
            user_id:
              type: string
              example: test1
              description: 사용자 ID
            password:
              type: string
              example: "111111"
              description: 사용자 비밀번호
    responses:
      200:
        description: 로그인 성공
        schema:
          type: object
          properties:
            message:
              type: string
              example: 로그인 성공
            token:
              type: string
              example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoidGVzdDEiLCJleHAiOjE2ODg2MzM4MDAsImlhdCI6MTY4ODYzMDAwMH0.uHvklwKBBzDl7R_kNHhjCMVPlUSfs1EoTxHqXW2HV6g"
      401:
        description: 인증 실패 (user_id 또는 비밀번호 오류)
        schema:
          type: object
          properties:
            error:
              type: string
              example: user_id 또는 비밀번호가 잘못되었습니다.
      500:
        description: 데이터베이스 작업 중 에러 발생
        schema:
          type: object
          properties:
            error:
              type: string
              example: 데이터베이스 에러 메시지
    """    
    data = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "SELECT user_id, password FROM users WHERE user_id = %s"
            cursor.execute(sql, (data["user_id"],))
            user = cursor.fetchone()

        if not user or not check_password(data["password"], user["password"]):
            return jsonify({"error": "user_id 또는 비밀번호가 잘못되었습니다."}), 401

        token = create_jwt_token(user["user_id"])
        return jsonify({"message": "로그인 성공", "token": token}), 200
    except pymysql.MySQLError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


# 토큰 갱신
# 미들웨어가 적용
@auth_bp.route("/auth/token/refresh", methods=["POST"])
#@swag_from('docs/auth.yml')
@token_required
def refresh_token():
    try:
        # g 객체에서 user_id 가져오기
        token = create_jwt_token(g.user_id)
        return jsonify({"message": "토큰 갱신 성공", "token": token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


'''
http://127.0.0.1:5000/auth/protected
'''
# 보호된 경로 예제
@auth_bp.route("/auth/protected", methods=["GET"])
@token_required
def protected_route():
    return jsonify({"message": "인증된 사용자만 접근 가능합니다.", "user_id": g.user_id}), 200

# 회원 정보 조회 API(완료)
'''
Req:
http://127.0.0.1:5000/auth/profile/test1

Res:
{
    "created_at": "Sun, 15 Dec 2024 14:32:29 GMT",
    "email": "test1@example.com",
    "name": "name1",
    "user_id": "test1"
}


'''
@auth_bp.route('/auth/profile/<string:user_id>', methods=['GET'])
#@swag_from('docs/auth.yml')
def auth_user(user_id):
    """
    회원 정보 조회 API
    ---
    tags:
      - "Authentication(회원가입/로그인 관련 API)"
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: 조회할 사용자 ID
    responses:
      200:
        description: 사용자 정보 조회 성공
        schema:
          type: object
          properties:
            user_id:
              type: string
              description: 사용자 ID
            email:
              type: string
              description: 이메일 주소
            name:
              type: string
              description: 사용자 이름
            created_at:
              type: string
              description: 생성 날짜 (ISO 형식)
        examples:
          application/json: |
            {
              "user_id": "test1",
              "email": "test1@example.com",
              "name": "Kim Hyuna",
              "created_at": "2024-12-15T14:32:29Z"
            }
      404:
        description: 사용자를 찾을 수 없음
        schema:
          type: object
          properties:
            message:
              type: string
        examples:
          application/json: |
            {
              "message": "사용자를 찾을 수 없습니다."
            }
      500:
        description: 서버 오류
        schema:
          type: object
          properties:
            error:
              type: string
        examples:
          application/json: |
            {
              "error": "Internal Server Error"
            }
    """
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
#@swag_from('docs/auth.yml')
def autu_update_user(user_id):
    
    """
    회원 정보 수정 API
    ---
    tags:
      - "Authentication(회원가입/로그인 관련 API)"
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: 수정할 사용자 ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              example: "newemail@example.com"
            name:
              type: string
              example: "New Name"
    responses:
      200:
        description: 회원 정보 수정 성공
        schema:
          type: object
          properties:
            message:
              type: string
        examples:
          application/json: |
            {
              "message": "회원 정보 수정 성공"
            }
      400:
        description: 잘못된 요청
        schema:
          type: object
          properties:
            error:
              type: string
        examples:
          application/json: |
            {
              "error": "Invalid request format"
            }
      500:
        description: 서버 오류
        schema:
          type: object
          properties:
            error:
              type: string
        examples:
          application/json: |
            {
              "error": "Internal Server Error"
            }
    """
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
    ---
    tags:
      - "Authentication(회원가입/로그인 관련 API)"
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: 비밀번호를 변경할 사용자 ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            current_password:
              type: string
              description: "현재 비밀번호"
              example: "oldpassword123"
            new_password:
              type: string
              description: "새 비밀번호"
              example: "newpassword123"
    responses:
      200:
        description: 비밀번호 변경 성공
        schema:
          type: object
          properties:
            message:
              type: string
        examples:
          application/json:
            {
              "message": "비밀번호 변경 성공"
            }
      400:
        description: 현재 비밀번호가 일치하지 않음
        schema:
          type: object
          properties:
            error:
              type: string
        examples:
          application/json:
            {
              "error": "현재 비밀번호가 일치하지 않습니다."
            }
      404:
        description: user_id가 존재하지 않음
        schema:
          type: object
          properties:
            error:
              type: string
        examples:
          application/json:
            {
              "error": "해당 user_id가 존재하지 않습니다."
            }
      500:
        description: 서버 오류
        schema:
          type: object
          properties:
            error:
              type: string
        examples:
          application/json:
            {
              "error": "Internal Server Error"
            }
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

            # 기존 비밀번호가 일치하는지 확인
            if not check_password(data['current_password'], user['password']):
                return jsonify({"error": "현재 비밀번호가 일치하지 않습니다."}), 400

            # 새 비밀번호를 암호화 후 업데이트
            new_password_encoded = hash_password(data['new_password'])
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
#@swag_from('docs/auth.yml')
def delete_user(user_id):
    
    """
    회원 탈퇴 API
    ---
    tags:
      - "Authentication(회원가입/로그인 관련 API)"
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: 탈퇴할 사용자 ID
    responses:
      200:
        description: 회원 탈퇴 성공
        schema:
          type: object
          properties:
            message:
              type: string
        examples:
          application/json: |
            {
              "message": "회원 탈퇴 성공"
            }
      404:
        description: user_id가 존재하지 않음
        schema:
          type: object
          properties:
            error:
              type: string
        examples:
          application/json: |
            {
              "error": "해당 user_id가 존재하지 않습니다."
            }
      500:
        description: 서버 오류
        schema:
          type: object
          properties:
            error:
              type: string
        examples:
          application/json: |
            {
              "error": "Internal Server Error"
            }
    """
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
    
