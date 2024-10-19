from flask_restx import Resource, Namespace, reqparse
from model import *
from flask import request

import json
import mysql.connector

# 데이터베이스 설정을 파일에서 불러옵니다.
with open('config/db_config.json', 'r') as f:
    db_config = json.load(f)

dashboard_ns = Namespace('dashboard', description='Dashboard API', doc='/dashboard', path='/dashboard')
dashboard_field = dashboard_ns.model('DashboardModel', dashboard_model)


@dashboard_ns.route('/register')
class RegisterResource(Resource):
    @dashboard_ns.expect(dashboard_field, validate=True)
    def post(self):
        """
        대시보드 등록
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json

        required_keys = ['name', 'gender', 'birth']

        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        name = data['name']
        gender = data['gender']
        birth = data['birth']
        location = data['location']

        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()
        try:
            # 대시보드 등록
            query = "INSERT INTO dashboard (name, gender, birth, location) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, gender, birth, location))
            person_id = cursor.lastrowid

            db.commit()

            return {
                'message': 'Dashboard registered successfully',
                'personId': person_id  # personId를 응답에 포함
            }, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()


@dashboard_ns.route('/delete/<int:person_id>/<string:name>')
class DeleteResource(Resource):
    def delete(self, person_id, name):
        """
        대시보드 삭제
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
            # 대시보드 삭제
            query = "DELETE FROM dashboard WHERE (name = %s and personId = %s)"
            cursor.execute(query, (name, person_id))

            db.commit()

            return {'message': 'Dashboard deleted successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()


@dashboard_ns.route('/<int:person_id>')
class GetDashboradResource(Resource):
    def get(self, person_id):
        """
        대시보드 조회
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
            query = "SELECT * FROM dashboard WHERE personId = %s"
            cursor.execute(query, (person_id,))
            dashboard = cursor.fetchone()

            if not dashboard:
                return {'message': 'Dashboard not found'}, 404

            dashboard_data = {
                'personId': dashboard[0],
                'name': dashboard[1],
                'gender': dashboard[2],
                'birth': dashboard[3].strftime('%Y-%m-%d'),
                'location': dashboard[4],
                'status': dashboard[5]
            }
            return {'dashboard': dashboard_data}, 200
        except Exception as e:
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()


@dashboard_ns.route('/update/<int:person_id>')
class UpdateResource(Resource):
    @dashboard_ns.expect(dashboard_field, validate=True)
    def put(self, person_id):
        """
        대시보드 수정
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json

        required_keys = ['name', 'gender', 'birth']

        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        name = data['name']
        gender = data['gender']
        birth = data['birth']
        location = data['location']

        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()
        try:
            # 대시보드 수정
            query = "UPDATE dashboard SET name = %s, gender = %s, birth = %s, location = %s WHERE personId = %s"
            cursor.execute(query, (name, gender, birth, location, person_id))
            db.commit()

            return {'message': 'Dashboard updated successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()


@dashboard_ns.route('/update/state/<int:person_id>')
class UpdateState(Resource):
    def put(self, person_id):
        """
        Person 상태 수정
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json

        required_keys = ['status']

        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        state = data['status']

        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()
        try:
            # 대시보드 상태 수정
            query = "UPDATE dashboard SET status = %s WHERE personId = %s"
            cursor.execute(query, (state, person_id))
            db.commit()

            return {'message': 'Dashboard state updated successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()
