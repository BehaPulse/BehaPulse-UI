from flask_restx import Resource, Namespace, reqparse
from model import *
from flask import request

import json
import mysql.connector

# 데이터베이스 설정을 파일에서 불러옵니다.
with open('config/db_config.json', 'r') as f:
    db_config = json.load(f)

user_dashboard_device_ns = Namespace('user_dashboard_device', description='User Dashboard Device API',
                                     doc='/user_dashboard_device',
                                     path='/user_dashboard_device')

user_dashboard_device_field = user_dashboard_device_ns.model('UserDashboardDeviceModel', user_dashboard_device_model)


@user_dashboard_device_ns.route('/register')
class RegisterResource(Resource):
    @user_dashboard_device_ns.expect(user_dashboard_device_field, validate=True)
    def post(self):
        """
        유저 대시보드 디바이스 등록
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json

        required_keys = ['userEmail', 'personId', 'deviceId']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        user_email = data['userEmail']
        person_id = data['personId']
        device_id = data['deviceId']

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

            # 대시보드 존재 여부 확인
            query = "SELECT * FROM dashboard WHERE personId = %s"
            cursor.execute(query, (person_id,))
            existing_dashboard = cursor.fetchone()

            if not existing_dashboard:
                return {'message': 'Dashboard not found'}, 404

            # 디바이스 존재 여부 확인
            query = "SELECT * FROM device WHERE deviceId = %s"
            cursor.execute(query, (device_id,))
            existing_device = cursor.fetchone()

            if not existing_device:
                return {'message': 'Device not found'}, 404

            # 기존 유저 대시보드 디바이스 존재 여부 확인
            query = "SELECT * FROM user_dashboard_device WHERE userEmail = %s AND personId = %s AND deviceId = %s"
            cursor.execute(query, (user_email, person_id, device_id))
            existing_user_dashboard_device = cursor.fetchone()

            if existing_user_dashboard_device:
                return {'message': 'User dashboard device already exists'}, 400

            # 유저 대시보드 디바이스 등록
            query = "INSERT INTO user_dashboard_device (userEmail, personId, deviceId) VALUES (%s, %s, %s)"
            cursor.execute(query, (user_email, person_id, device_id))
            db.commit()

            return {'message': 'User dashboard device registered successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()


@user_dashboard_device_ns.route('/user_dashboard_devices/<string:userEmail>')
class GetUserDashboardDevice(Resource):
    def get(self, userEmail):
        """
        유저 대시보드 디바이스 리스트 가져오기
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
            query = "SELECT * FROM user_dashboard_device WHERE userEmail = %s"
            cursor.execute(query, (userEmail,))
            user_dashboard_devices = cursor.fetchall()

            if not user_dashboard_devices:
                return {'message': 'User dashboard devices not found'}, 404

            return {'user_dashboard_device': [
                {
                    'userEmail': user_dashboard_device[1],
                    'personId': user_dashboard_device[2],
                    'deviceId': user_dashboard_device[3]
                }
                for user_dashboard_device in user_dashboard_devices
            ]}, 200

        except Exception as e:
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()


@user_dashboard_device_ns.route('/user_dashboard_devices/person/<string:userEmail>/<int:deviceId>')
class GetUserId(Resource):
    def get(self, userEmail, deviceId):
        """
        유저 대시보드 PersonId 조회
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
            query = "SELECT * FROM user_dashboard_device WHERE userEmail = %s AND deviceId = %s"
            cursor.execute(query, (userEmail, deviceId))
            user_dashboard_device = cursor.fetchone()

            if not user_dashboard_device:
                return {'message': 'User dashboard device not found'}, 404

            return {'user_dashboard_device': user_dashboard_device}, 200

        except Exception as e:
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()


@user_dashboard_device_ns.route('/user_dashboard_devices/device/<string:userEmail>/<int:personId>')
class GetDeviceId(Resource):
    def get(self, userEmail, personId):
        """
        유저 대시보드 디바이스Id 조회
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
            query = "SELECT * FROM user_dashboard_device WHERE userEmail = %s AND personId = %s"
            cursor.execute(query, (userEmail, personId))
            user_dashboard_device = cursor.fetchall()

            if not user_dashboard_device:
                return {'message': 'User dashboard device not found'}, 404

            return {'user_dashboard_device': user_dashboard_device}, 200

        except Exception as e:
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()


@user_dashboard_device_ns.route('/update/<string:userEmail>/<int:deviceId>')
class UpdateResource(Resource):
    def put(self, userEmail, deviceId):
        """
        유저 대시보드 디바이스 수정
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json
        if 'userEmail' not in data or 'deviceId' not in data or 'personId' not in data:
            return {'message': 'Missing required fields'}, 400

        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()

        try:
            # 유저 대시보드 디바이스 존재 여부 확인
            query = "SELECT * FROM user_dashboard_device WHERE userEmail = %s AND deviceId = %s"
            cursor.execute(query, (userEmail, deviceId))
            existing_user_dashboard_device = cursor.fetchone()

            if not existing_user_dashboard_device:
                return {'message': 'User dashboard device not found'}, 404

            # 유저 대시보드 디바이스 수정
            query = "UPDATE user_dashboard_device SET userEmail = %s, deviceId = %s, personId = %s WHERE userEmail = %s AND deviceId = %s"
            cursor.execute(query, (data['userEmail'], data['deviceId'], data['personId'], userEmail, deviceId))
            db.commit()

            return {'message': 'User dashboard device updated successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()

@user_dashboard_device_ns.route('/user_dashboard_devices/<string:userEmail>/<string:location>')
class GetUserDashboardDevice(Resource):
    def get(self, userEmail, location):
        """
        유저 대시보드에서 장치가 설치된 위치 리스트 가져오기
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
            query = """select * from user_dashboard_device udd            
            join device d on udd.deviceId = d.deviceId
            where udd.userEmail = %s and d.install_location = %s           
            """
            cursor.execute(query, (userEmail, location))
            user_dashboard_devices = cursor.fetchall()

            if not user_dashboard_devices:
                return {'message': 'User dashboard devices not found'}, 404

            return {'user_dashboard_device': [
            {
                 'userEmail': user_dashboard_device[1],
                 'personId': user_dashboard_device[2],
                 'deviceId': user_dashboard_device[3],
            }
            for user_dashboard_device in user_dashboard_devices
            ]}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()