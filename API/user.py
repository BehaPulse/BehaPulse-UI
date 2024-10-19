from flask_restx import Resource, Namespace, reqparse
from model import *
from flask import request

from datetime import datetime

import json
import mysql.connector
import random
import string

# 데이터베이스 설정을 파일에서 불러옵니다.
with open('config/db_config.json', 'r') as f:
    db_config = json.load(f)

user_ns = Namespace('user', description='User API', doc='/user', path='/user')
user_field = user_ns.model('UserModel', user_model)
login_field = user_ns.model('LoginModel', login_model)
security_question_field = user_ns.model('SecurityQuestionModel', security_question_model)
st_token_field = user_ns.model('SmartThingsTokenModel', st_token_model)

@user_ns.route('/register')
class RegisterResource(Resource):
    @user_ns.expect(user_field, validate=True)
    def post(self):
        """
        유저 등록
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json

        required_keys = ['userEmail', 'userPassword', 'userGender', 'userName', 'securityQuestion', 'securityAnswer',
                         'birthDate']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        email = data['userEmail']
        password = data['userPassword']
        name = data['userName']
        gender = data['userGender']
        security_question = data['securityQuestion']
        security_answer = data['securityAnswer']
        birth_date = data['birthDate']

        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()
        try:
            # 기존 유저 존재 여부 확인
            query = "SELECT * FROM user WHERE userEmail = %s"
            cursor.execute(query, (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                return {'message': 'user already exists'}, 400

            # 유저 등록
            query = "INSERT INTO user (userEmail, userPassword, userGender, userName, securityQuestion, securityAnswer, birthday) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (email, password, gender, name, security_question, security_answer, birth_date))
            db.commit()

            return {'message': 'user registered successfully'}, 201

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()


@user_ns.route('/login')
class LoginResource(Resource):
    @user_ns.expect(login_field, validate=True)
    def post(self):
        """
        유저 로그인
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json

        required_keys = ['userEmail', 'userPassword']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        email = data['userEmail']
        password = data['userPassword']

        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()
        try:
            # 유저 존재 여부 확인
            query = "SELECT * FROM user WHERE userEmail = %s AND userPassword = %s"
            cursor.execute(query, (email, password))
            user = cursor.fetchone()

            if not user:
                return {'message': 'user not found'}, 404

            return {'userName': user[2]}, 200

        except Exception as e:
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()


@user_ns.route('/find_password/<string:userEmail>')
class FindPasswordResource(Resource):
    def get(self, userEmail):
        """
        비밀번호 찾기
        """
        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()
        try:
            query = "SELECT securityQuestion FROM user WHERE userEmail = %s"
            cursor.execute(query, (userEmail,))
            security_question = cursor.fetchone()

            if not security_question:
                return {'message': 'user not found'}, 404

            return {'securityQuestion': security_question[0]}, 200

        except Exception as e:
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()

    @user_ns.expect(security_question_field, validate=True)
    def post(self, userEmail):
        """
        비밀번호 찾기
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json

        required_keys = ['securityQuestion', 'securityAnswer']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        security_question = data['securityQuestion']
        security_answer = data['securityAnswer']

        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()

        try:
            # 보안 질문과 답변을 확인하여 유저 존재 여부를 체크
            query = ("SELECT userPassword FROM user "
                     "WHERE userEmail = %s AND securityAnswer = %s AND securityQuestion = %s")
            cursor.execute(query, (userEmail, security_answer, security_question))
            user_password = cursor.fetchone()

            if not user_password:
                return {'message': 'User not found or security answer incorrect.'}, 404

            # 임시 비밀번호 생성
            temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

            # 임시 비밀번호를 DB에 업데이트
            update_query = "UPDATE user SET userPassword = %s WHERE userEmail = %s"
            cursor.execute(update_query, (temp_password, userEmail))
            db.commit()

            return {'temporaryPassword': temp_password}, 200

        except Exception as e:
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()


@user_ns.route('/delete/<string:userEmail>')
class DeleteUserResource(Resource):
    def delete(self, userEmail):
        """
        특정 유저 삭제
        """
        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()
        try:
            # 유저 존재 여부 확인
            query = "SELECT * FROM user WHERE userEmail = %s"
            cursor.execute(query, (userEmail,))
            existing_user = cursor.fetchone()

            if not existing_user:
                return {'message': 'User not found'}, 404

            # 유저 삭제
            query = "DELETE FROM user WHERE userEmail = %s"
            cursor.execute(query, (userEmail,))
            db.commit()

            return {'message': 'User deleted successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500
        finally:
            db.close()
            cursor.close()


@user_ns.route('/<string:userEmail>')
class GetUserResource(Resource):
    def get(self, userEmail):
        """
        특정 유저 조회
        """
        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()

        try:
            # 유저 존재 여부 확인
            query = "SELECT * FROM user WHERE userEmail = %s"
            cursor.execute(query, (userEmail,))
            user = cursor.fetchone()

            if not user:
                return {'message': 'User not found'}, 404

            user_data = {
                'userEmail': user[0],
                'userName': user[2],
                'createdAt': user[3].strftime('%Y-%m-%d'),
                'securityQuestion': user[4],
                'securityAnswer': user[5],
                'gender': user[6],
                'birthDate': user[7].strftime('%Y-%m-%d')
            }

            return {'user': user_data}, 200

        except Exception as e:
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()


@user_ns.route('/check-email/<string:userEmail>')
class CheckEmailResource(Resource):
    def get(self, userEmail):
        """
        이메일 존재 여부 확인
        """
        # 데이터베이스 연결
        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()

        try:
            # 이메일 존재 여부 확인 쿼리
            query = "SELECT userEmail FROM user WHERE userEmail = %s"
            cursor.execute(query, (userEmail,))
            user = cursor.fetchone()

            if user:
                return {'message': '해당 이메일이 존재합니다.', 'exists': True}, 200
            else:
                return {'message': '해당 이메일이 존재하지 않습니다.', 'exists': False}, 404

        except Exception as e:
            return {'message': str(e)}, 500

        finally:
            cursor.close()
            db.close()


@user_ns.route('/find_id/<string:userName>/<string:birthday>')
class FindPasswordResource(Resource):
    def get(self, userName, birthday):
        """
        이메일 찾기
        """
        # 데이터베이스 연결
        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()

        # 날짜 형식 검증 ('YYYY-MM-DD' 형식으로 변환)
        try:
            formatted_birthday = datetime.strptime(birthday, '%Y-%m-%d').strftime('%Y-%m-%d')
        except ValueError:
            return {'message': 'Invalid date format. Use YYYY-MM-DD.'}, 400

        try:
            # 이메일 존재 여부 확인 쿼리
            query = "SELECT userEmail FROM user WHERE userName = %s AND birthday = %s"
            cursor.execute(query, (userName, formatted_birthday))

            # 여러 결과를 처리하기 위해 fetchall() 사용
            users = cursor.fetchall()

            if users:
                # 여러 개의 이메일이 있을 수 있으므로 리스트로 반환
                emails = [user[0] for user in users]
                return {'message': '해당 이메일이 존재합니다.', 'exists': True, 'userEmails': emails}, 200
            else:
                return {'message': '해당 이메일이 존재하지 않습니다.', 'exists': False}, 404

        except Exception as e:
            return {'message': str(e)}, 500

        finally:
            cursor.close()
            db.close()


@user_ns.route('/update/password/<string:userEmail>')
class changePasswordResource(Resource):
    def put(self, userEmail):
        """
        비밀번호 변경
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json

        required_keys = ['oldPassword', 'newPassword']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        old_password = data['oldPassword']
        new_password = data['newPassword']

        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()

        try:
            # 이전 비밀번호 일치 여부 확인
            query = "SELECT userPassword FROM user WHERE userEmail = %s"
            cursor.execute(query, (userEmail,))
            user_password = cursor.fetchone()

            if not user_password:
                return {'message': 'User not found'}, 404

            if user_password[0] != old_password:
                return {'message': 'Old password incorrect'}, 400

            # 비밀번호 변경
            update_query = "UPDATE user SET userPassword = %s WHERE userEmail = %s"
            cursor.execute(update_query, (new_password, userEmail))
            db.commit()

            return {'message': 'Password updated successfully'}, 200

        except Exception as e:
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()


@user_ns.route('/delete_st_token/<string:userEmail>')
class DeleteTokenResource(Resource):
    def delete(self, userEmail):
        """
        등록되어 있던 SmartThings Token 삭제 (access_token, refresh_token)
        """
        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()
        try:
            # 유저 존재 여부 확인
            query = "SELECT * FROM user WHERE userEmail = %s"
            cursor.execute(query, (userEmail,))
            existing_user = cursor.fetchone()

            if not existing_user:
                return {'message': 'User not found'}, 404

            # 토큰 삭제 (null로 설정)
            query = "UPDATE user SET stAccessToken = NULL, stRefreshToken = NULL WHERE userEmail = %s"
            cursor.execute(query, (userEmail,))
            db.commit()

            return {'message': 'successfully delete token'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500
        finally:
            db.close()
            cursor.close()


@user_ns.route('/st_token/<string:userEmail>')
class GetTokenResource(Resource):
    def get(self, userEmail):
        """
        특정 유저의 토큰 조회
        """
        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()

        try:
            query = "SELECT stAccessToken, stRefreshToken FROM user WHERE userEmail = %s"
            cursor.execute(query, (userEmail,))
            user = cursor.fetchone()

            if not user:
                return {'message': 'User not found'}, 404

            user_data = {
                'stAccessToken': user[0],
                'stRefreshToken': user[1],
            }

            return {'user': user_data}, 200

        except Exception as e:
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()


@user_ns.route('/set_st_token/<string:userEmail>')
class SetTokenResource(Resource):
    @user_ns.expect(st_token_field, validate=True)
    def post(self, userEmail):
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json

        required_keys = ['stAccessToken', 'stRefreshToken']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        stAccessToken = data['stAccessToken']
        stRefreshToken = data['stRefreshToken']

        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()
        try:
            query = "UPDATE user SET stAccessToken = %s, stRefreshToken = %s WHERE userEmail = %s"
            cursor.execute(query, (stAccessToken, stRefreshToken, userEmail,))
            db.commit()

            return {'message': 'user registered successfully'}, 201

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()