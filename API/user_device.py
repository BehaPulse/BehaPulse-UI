from flask_restx import Resource, Namespace, reqparse
from model import *
from flask import request
import json
import mysql.connector

# 데이터베이스 설정을 파일에서 불러옵니다.
with open('config/db_config.json', 'r') as f:
    db_config = json.load(f)

user_device_ns = Namespace('user_device', description='User Device API', doc='/user_device', path='/user_device')
user_device_field = user_device_ns.model('UserDeviceModel', user_device_model)


@user_device_ns.route('/register')
class RegisterResource(Resource):
    @user_device_ns.expect(user_device_field, validate=True)
    def post(self):
        """
        유저 디바이스 등록
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json

        required_keys = ['userEmail', 'macAddress']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        user_email = data['userEmail']
        mac_address = data['macAddress']

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

            # 디바이스 존재 여부 확인 및 deviceId 가져오기
            query = "SELECT deviceId FROM device WHERE macAddress = %s"
            cursor.execute(query, (mac_address,))
            existing_device = cursor.fetchone()

            if not existing_device:
                return {'message': 'Device not found'}, 404

            device_id = existing_device[0]

            # 기존 유저 디바이스 존재 여부 확인
            query = "SELECT * FROM user_device WHERE userEmail = %s AND deviceId = %s"
            cursor.execute(query, (user_email, device_id))
            existing_user_device = cursor.fetchone()

            if existing_user_device:
                return {'message': 'User device already exists'}, 400

            # 유저 디바이스 등록
            query = "INSERT INTO user_device (userEmail, deviceId) VALUES (%s, %s)"
            cursor.execute(query, (user_email, device_id))
            db.commit()

            return {'message': 'User device registered successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()


@user_device_ns.route('/user_devices')
class UserDeviceResource(Resource):
    def get(self):
        """
        모든 유저 디바이스 조회
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
            query = "SELECT * FROM user_device"
            cursor.execute(query)
            user_devices = cursor.fetchall()

            if not user_devices:
                return {'message': 'No user device found'}, 404

            return {'user_devices': user_devices}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()


@user_device_ns.route('/user_devices/<string:userEmail>')
class GetUserDeviceResource(Resource):
    def get(self, userEmail):
        """
        특정 유저의 디바이스 조회
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
            query = "SELECT * FROM user_device WHERE userEmail = %s"
            cursor.execute(query, (userEmail,))
            user_devices = cursor.fetchall()

            if not user_devices:
                return {'message': 'No user device found'}, 404

            return {'user_devices': user_devices}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500
        finally:
            db.close()
            cursor.close()


@user_device_ns.route('/delete/<string:userEmail>/<string:macAddress>')
class DeleteUserDeviceResource(Resource):
    def delete(self, userEmail, macAddress):
        """
        유저 디바이스 삭제
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
            # 디바이스 존재 여부 확인 및 deviceId 가져오기
            query = "SELECT deviceId FROM device WHERE macAddress = %s"
            cursor.execute(query, (macAddress,))
            existing_device = cursor.fetchone()

            if not existing_device:
                return {'message': 'Device not found'}, 404

            device_id = existing_device[0]

            # 유저 디바이스 존재 여부 확인
            query = "SELECT * FROM user_device WHERE userEmail = %s AND deviceId = %s"
            cursor.execute(query, (userEmail, device_id))
            existing_user_device = cursor.fetchone()

            if not existing_user_device:
                return {'message': 'User device not found'}, 404

            # 유저 디바이스 삭제
            query = "DELETE FROM user_device WHERE userEmail = %s AND deviceId = %s"
            cursor.execute(query, (userEmail, device_id))
            db.commit()

            return {'message': 'User device deleted successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()


@user_device_ns.route('/<int:deviceId>')
class getEmail(Resource):
    def get(self, deviceId):
        """
        특정 디바이스의 이메일 조회
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
            query = "SELECT * FROM user_device WHERE deviceId = %s"
            cursor.execute(query, (deviceId,))
            user_device = cursor.fetchone()

            if not user_device:
                return {'message': 'User device not found'}, 404

            return {'user_device': user_device}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500
        finally:
            db.close()
            cursor.close()


@user_device_ns.route('/user_devices_with_details/<string:userEmail>')
class GetUserDeivceWithDetailsResource(Resource):
    def get(self, userEmail):
        """
            특정 유저의 모든 디바이스와 상세 정보 조회 (JOIN 사용)
        """
        # 데이터베이스 연결
        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor(dictionary=True)  # 결과를 딕셔너리 형태로 반환
        try:
            query = """ SELECT d.deviceId, d.macAddress, d.type, d.install_location, d.room,
                       d.check_date, d.on_off, d.note
                       FROM user_device ud
                       JOIN device d ON ud.deviceId = d.deviceId
                       WHERE ud.userEmail = %s
                """
            cursor.execute(query, (userEmail,))
            devices = cursor.fetchall()

            if not devices:
                return {'message': 'No user devices found'}, 404
                # 장치 데이터를 리스트에 추가

            # 딕셔너리 목록을 반환하여 간소화
            return {'user_devices': [
                {
                    'location': device['install_location'],
                    'room': device['room'],
                    'macAddress': device['macAddress'],
                    'type': device['type'],
                    'on_off': device['on_off']
                }
                for device in devices
            ]}, 200

        except Exception as e:
            return {'message': str(e)}, 500
        finally:
            db.close()
            cursor.close()

@user_device_ns.route('/user_devices_with_location/<string:userEmail>')
class GetUserDeviceWithLocationResource(Resource):
    def get(self, userEmail):
        """
        특정 유저의 모든 디바이스와 위치 정보 조회 (JOIN 사용)
        """
        # 데이터베이스 연결
        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor(dictionary=True)

        try:
            query = """ SELECT d.install_location
                              FROM user_device ud
                              JOIN device d ON ud.deviceId = d.deviceId
                              WHERE ud.userEmail = %s
                       """
            cursor.execute(query, (userEmail,))
            devices = cursor.fetchall()

            if not devices:
                return {'message': 'No user devices found'}, 404
                # 장치 데이터를 리스트에 추가

            # 유니크한 장소의 이름만 목록으로 return
            return {'location': list(set([device['install_location'] for device in devices]))}, 200

        except Exception as e:
            return {'message': str(e)}, 500
        finally:
            db.close()
            cursor.close()

