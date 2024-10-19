import collections

from flask_restx import Resource, Namespace, reqparse
from model import *

from flask import request, jsonify
import json
import mysql.connector
import math

# 데이터베이스 설정을 파일에서 불러옵니다.
with open('config/db_config.json', 'r') as f:
    db_config = json.load(f)

device_ns = Namespace('device', description='Device API', doc='/device', path='/device')
device_field = device_ns.model('DeviceModel', device_model)


@device_ns.route('/register')
class RegisterResource(Resource):
    @device_ns.expect(device_field, validate=True)
    def post(self):
        """
        디바이스 등록
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json

        required_keys = ['macAddress', 'type']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        mac_address = data['macAddress']
        device_type = data['type']
        install_location = data['install_location']
        room = data['room']
        check_date = data['check_date']
        on_off = data['on_off']
        note = data['note']

        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()
        try:

            # MAC 주소 중복 확인
            query = "SELECT * FROM device WHERE macAddress = %s"
            cursor.execute(query, (mac_address,))
            existing_device = cursor.fetchone()

            if existing_device:
                return {'message': 'Device with this MAC address already exists'}, 400

            # 디바이스 등록
            query = "INSERT INTO device (macAddress, type, install_location, room, check_date, note, on_off) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (mac_address, device_type, install_location, room, check_date, note, on_off))
            db.commit()

            return {'message': 'Device registered successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()


@device_ns.route('/delete/<string:macAddress>')
class DeleteDeviceResource(Resource):
    def delete(self, macAddress):
        """
        디바이스 삭제
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
            query = "DELETE FROM device WHERE macAddress = %s"
            cursor.execute(query, (macAddress,))
            db.commit()

            return {'message': 'Device deleted successfully'}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()


@device_ns.route('/<int:deviceId>')
class GetDeviceResource(Resource):
    def get(self, deviceId):
        """
        특정 디바이스 조회
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
            query = "SELECT * FROM device WHERE deviceId = %s"
            cursor.execute(query, (deviceId,))
            device = cursor.fetchone()

            if not device:
                return {'message': 'Device not found'}, 404

            device_data = {
                'deviceId': device[0],
                'macAddress': device[1],
                'type': device[2],
                'install_location': device[3],
                'room': device[4],
                'check_date': device[5].strftime('%Y-%m-%d'),
                'on_off': device[6],
                'note': device[7],
            }
            return {'device': device_data}, 200

        except Exception as e:
            db.rollback()  # 롤백 전에 현재 커서의 명령이 완료되었는지 확인
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()


@device_ns.route('/<string:macAddress>')
class GetDeviceResource(Resource):
    def get(self, macAddress):
        """
        특정 디바이스 조회
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
            query = "SELECT * FROM device WHERE macAddress = %s"
            cursor.execute(query, (macAddress,))
            device = cursor.fetchone()

            if not device:
                return {'message': 'Device not found'}, 404

            device_data = {
                'deviceId': device[0],
                'macAddress': device[1],
                'type': device[2],
                'install_location': device[3],
                'room': device[4],
                'check_date': device[5].strftime('%Y-%m-%d'),
                'on_off': device[6],
                'note': device[7],
            }
            return {'device': device_data}, 200

        except Exception as e:
            db.rollback()

        finally:
            db.close()
            cursor.close()


@device_ns.route('/update/<string:macAddress>')
class UpdateDeviceResource(Resource):
    @device_ns.expect(device_field, validate=True)
    def put(self, macAddress):
        """
        특정 디바이스 정보 수정
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json

        required_keys = ['type']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        macAddress = macAddress
        device_type = data['type']
        install_location = data['install_location']
        room = data['room']
        check_date = data['check_date']
        on_off = data['on_off']
        note = data['note']

        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()
        try:
            query = "UPDATE device SET type = %s, install_location = %s, room = %s, check_date = %s, note = %s, " \
                    "on_off = %s WHERE macAddress = %s"
            cursor.execute(query, (device_type, install_location, room, check_date, note, on_off, macAddress))
            db.commit()

            # 수정한 행을 반환
            query = "SELECT * FROM device WHERE macAddress = %s"
            cursor.execute(query, (macAddress,))
            device = cursor.fetchone()

            device_data = {
                'deviceId': device[0],
                'macAddress': device[1],
                'type': device[2],
                'install_location': device[3],
                'room': device[4],
                'check_date': device[5].strftime('%Y-%m-%d'),
                'on_off': device[6],
                'note': device[7],
            }

            return {'message': 'Device updated successfully', 'device': device_data}, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500

        finally:
            db.close()
            cursor.close()


csi_data_dict = collections.defaultdict(lambda: {'amp': collections.deque(maxlen=100)})


def process_csi_data(line):
    global csi_data_dict
    if "CSI_DATA" in line:
        # Split the string to extract relevant parts
        all_data = line.split(',')
        mac_address = all_data[2]  # Extract the MAC address
        # print(mac_address)
        csi_data_str = all_data[-1].strip()[1:-1]  # Extract CSI data part and remove brackets
        csi_data = []
        # print(csi_data_str)
        # csi_data = list(map(int, csi_data_str.split()))
        for item in csi_data_str.split():
            try:
                csi_data.append(int(item))
            except ValueError:
                # print(f"Skipping invalid data: {item}")
                continue

        # print(csi_data)

        imaginary = csi_data[1::2]  # Extract imaginary parts (odd indices)
        real = csi_data[::2]  # Extract real parts (even indices)

        amplitudes = []
        if len(imaginary) > 0 and len(real) > 0:
            for j in range(len(imaginary)):
                amplitude_calc = math.sqrt(imaginary[j] ** 2 + real[j] ** 2)
                amplitudes.append(amplitude_calc)

            csi_data_dict[mac_address]['amp'].append(amplitudes)


@device_ns.route('/CSI')
class CSI(Resource):
    global csi_data_dict

    def post(self):
        if request.is_json:
            json_data = request.get_json()
            file_lines = json_data.get('file_lines', [])

            # Process each line in the received batch of file lines
            for line in file_lines:
                # print(line)
                process_csi_data(line)
                # print(csi_data_dict['78:21:84:BB:42:9C'])  # Process each line of CSI data
                # print(process_csi_data(line))
            return {'message': 'Batch of lines processed successfully',
                    'data': {'lines_processed': len(file_lines)}}, 200
        else:
            return {'message': 'Request body must be JSON'}, 400


@device_ns.route('/CSI/<string:mac_address>')
class LatestCSIData(Resource):
    global csi_data_dict

    def get(self, mac_address):
        if mac_address in csi_data_dict:
            return jsonify(list(csi_data_dict[mac_address]['amp']))
        else:
            return jsonify([])


@device_ns.route('/CSI/get_mac_addresses')
class MacAddresses(Resource):
    global csi_data_dict

    def get(self):
        return jsonify(list(csi_data_dict.keys()))
