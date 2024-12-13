from flask import Flask, request, jsonify
import pymysql
import base64
import json
from datetime import datetime

app = Flask(__name__)

# MySQL 데이터베이스 연결 함수
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='flask_user',
        password='555555',
        database='saramin_db',
        cursorclass=pymysql.cursors.DictCursor
    )

# 기본 루트 경로
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Flask API is running!"}), 200

# 회원가입 API(완료)
'''
{
    "user_id": "test1",
    "email": "john.doe@example.com",
    "password": "111111",
    "name": "John Doe"
}
'''
@app.route('/auth/register', methods=['POST'])
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
@app.route('/auth/login', methods=['POST'])
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
@app.route('/auth/profile/<string:user_id>', methods=['GET'])
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
@app.route('/autu/profile/<string:user_id>', methods=['PUT'])
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
@app.route('/auth/profile/change_password/<string:user_id>', methods=['PUT'])
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
@app.route('/autu/profile/<string:user_id>', methods=['DELETE'])
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

# 채용 공고 조회 API(완료)
@app.route('/jobs', methods=['GET'])
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
@app.route('/jobs/<int:job_id>', methods=['GET'])
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
@app.route('/jobs', methods=['POST'])
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
@app.route('/jobs/<int:job_id>', methods=['PUT'])
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
@app.route('/jobs/<int:job_id>', methods=['DELETE'])
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

# 관심 등록 API(완료)
'''
http://127.0.0.1:5000/favorites
{
    "user_id": "test2",
    "job_id": 10,
    "applied": false
}

'''
@app.route('/favorites', methods=['POST'])
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

            # favorites 테이블에 삽입
            sql = "INSERT INTO favorites (user_id, job_id) VALUES (%s, %s)"
            cursor.execute(sql, (data['user_id'], data['job_id']))
            conn.commit()

        return jsonify({"message": "관심 등록 성공"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# 사용자 관심 공고 조회 API(완료)
'''
http://127.0.0.1:5000/favorites/test3
'''
@app.route('/favorites/<string:user_id>', methods=['GET'])
def get_user_favorites(user_id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
            SELECT saramin_jobs.* 
            FROM favorites
            JOIN saramin_jobs ON favorites.job_id = saramin_jobs.id
            WHERE favorites.user_id = %s
            """
            cursor.execute(sql, (user_id,))
            favorites = cursor.fetchall()
        return jsonify(favorites), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# 지원하기 API(완료)
'''
http://127.0.0.1:5000/applications

{
    "user_id": "test3",
    "job_id": 55
}
'''
@app.route('/applications', methods=['POST'])  # URL이 '/apply_'로 명확히 매핑됨
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
@app.route('/applications/cancel', methods=['DELETE'])
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
@app.route('/applications/list/<string:user_id>', methods=['GET'])
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
        
        
#-------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)        