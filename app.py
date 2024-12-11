from flask import Flask, request, jsonify
import pymysql
import base64

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

# 회원가입 API
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 비밀번호 Base64 암호화
            encoded_password = base64.b64encode(data['password'].encode()).decode()
            sql = """
            INSERT INTO users (email, password, name) VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (data['email'], encoded_password, data['name']))
            conn.commit()
        return jsonify({"message": "회원가입 성공"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# 로그인 API
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 비밀번호 Base64 암호화
            encoded_password = base64.b64encode(data['password'].encode()).decode()
            sql = "SELECT * FROM users WHERE email=%s AND password=%s"
            cursor.execute(sql, (data['email'], encoded_password))
            user = cursor.fetchone()
        if user:
            return jsonify({"message": "로그인 성공", "user": user}), 200
        else:
            return jsonify({"message": "로그인 실패"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# 회원 정보 수정 API
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
            UPDATE users SET email=%s, name=%s WHERE id=%s
            """
            cursor.execute(sql, (data.get('email'), data.get('name'), user_id))
            conn.commit()
        return jsonify({"message": "회원 정보 수정 성공"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# 회원 탈퇴 API
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "DELETE FROM users WHERE id=%s"
            cursor.execute(sql, (user_id,))
            conn.commit()
        return jsonify({"message": "회원 탈퇴 성공"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# 채용 공고 조회 API
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

# 채용 공고 검색 API
@app.route('/jobs/search', methods=['GET'])
def search_jobs():
    keyword = request.args.get('keyword', '')
    location = request.args.get('location', '')
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            query = """
            SELECT * FROM saramin_jobs WHERE title LIKE %s OR company LIKE %s
            """
            params = [f"%{keyword}%", f"%{keyword}%"]
            if location:
                query += " AND location LIKE %s"
                params.append(f"%{location}%")
            cursor.execute(query, params)
            jobs = cursor.fetchall()
        return jsonify(jobs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# 채용 공고 등록 API
@app.route('/jobs', methods=['POST'])
def add_job():
    data = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO saramin_jobs (title, company, location, salary, description)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                data.get('title'), data.get('company'),
                data.get('location'), data.get('salary'),
                data.get('description')
            ))
            conn.commit()
        return jsonify({"message": "채용 공고 등록 성공"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# 채용 공고 삭제 API
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

# 관심 등록 API
@app.route('/favorites', methods=['POST'])
def add_favorite():
    data = request.json
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO favorites (user_id, job_id) VALUES (%s, %s)
            """
            cursor.execute(sql, (data['user_id'], data['job_id']))
            conn.commit()
        return jsonify({"message": "관심 등록 성공"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
