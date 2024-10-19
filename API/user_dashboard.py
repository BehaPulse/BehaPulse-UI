from flask_restx import Resource, Namespace, reqparse
from model import *
from flask import request

import json
import mysql.connector

# 데이터베이스 설정을 파일에서 불러옵니다.
with open('config/db_config.json', 'r') as f:
    db_config = json.load(f)

user_dashboard_ns = Namespace('user_dashboard', description='User Dashboard API', doc='/user_dashboard',
                              path='/user_dashboard')
user_dashboard_field = user_dashboard_ns.model('UserDashboardModel', user_dashboard_model)


@user_dashboard_ns.route('/register')
class RegisterResource(Resource):
    @user_dashboard_ns.expect(user_dashboard_field, validate=True)
    def post(self):
        """
        유저 대시보드 등록
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json

        required_keys = ['userEmail', 'personId']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        user_email = data['userEmail']
        person_id = data['personId']

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
            cursor.execute(query, (user_email,))
            existing_user = cursor.fetchone()

            if not existing_user:
                return {'message': 'User not found'}, 404

            # 기존 유저 대시보드 존재 여부 확인
            query = "SELECT * FROM user_dashboard WHERE userEmail = %s AND personId = %s"
            cursor.execute(query, (user_email, person_id))
            existing_user_dashboard = cursor.fetchone()

            if existing_user_dashboard:
                return {'message': 'User dashboard already exists'}, 400

            # 유저 대시보드 등록
            query = "INSERT INTO user_dashboard (userEmail, personId) VALUES (%s, %s)"
            cursor.execute(query, (user_email, person_id))

            db.commit()

            return {'message': 'User dashboard registered successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()


@user_dashboard_ns.route('/user_dashboards/<string:userEmail>')
class GetDashboardsResource(Resource):
    def get(self, userEmail):
        """
        유저 대시보드 리스트 가져오기
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
            query = "SELECT * FROM user_dashboard WHERE userEmail = %s"
            cursor.execute(query, (userEmail,))
            dashboards = cursor.fetchall()

            return {'dashboards': dashboards}, 200

        except Exception as e:
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()


@user_dashboard_ns.route('/delete/<string:userEmail>/<int:personId>')
class DeleteResource(Resource):
    def delete(self, userEmail, personId):
        """
        유저 대시보드 삭제
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
            query = "DELETE FROM user_dashboard WHERE (userEmail = %s and personId = %s)"
            cursor.execute(query, (userEmail, personId))

            db.commit()

            return {'message': 'User dashboard deleted successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()

@user_dashboard_ns.route('/user_dashboards_with_details/<string:userEmail>')
class GetDashboardsWithDetailsResource(Resource):
    def get(self, userEmail):
        """
        유저 대시보드 리스트 가져오기
        """
        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor(dictionary=True)
        try:
            query = """ select d.personId, d.name, d.gender, d.birth, d.location, d.status
                        from user_dashboard ud
                        join dashboard d on ud.personId = d.personId
                        WHERE ud.userEmail = %s
                """
            cursor.execute(query, (userEmail,))
            dashboards = cursor.fetchall()

            if not dashboards:
                return {'message': 'No user dashboard found'}, 404
                # 장치 데이터를 리스트에 추가

            # 딕셔너리 목록을 반환하여 간소화
            return {'dashboards': [
                {
                    'personId': dashboard['personId'],
                    'name': dashboard['name'],
                    'gender': dashboard['gender'],
                    'birth': dashboard['birth'].strftime('%Y-%m-%d'),
                    'status': dashboard['status'],
                }
                for dashboard in dashboards
            ]}, 200

        except Exception as e:
            return {'message': str(e)}, 500
        finally:
            db.close()
            cursor.close()