from flask_restx import Resource, Namespace, reqparse
from model import *
from flask import request

import json
import mysql.connector

# 데이터베이스 설정을 파일에서 불러옵니다.
with open('config/db_config.json', 'r') as f:
    db_config = json.load(f)

color_brightness_ns = Namespace('color_brightness', description='Color Brightness API', doc='/color_brightness',
                                path='/color_brightness')
color_brightness_field = color_brightness_ns.model('ColorBrightnessModel', color_brightness_model)


@color_brightness_ns.route('/register')
class RegisterResource(Resource):
    @color_brightness_ns.expect(color_brightness_field, validate=True)
    def post(self):
        """
        색상 및 밝기 등록
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json
        required_keys = ['color', 'brightness', 'status', 'personId']

        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        color = data['color']
        brightness = data['brightness']
        status = data['status']
        personId = data['personId']

        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()

        try:
            query = "SELECT * FROM color_brightness WHERE status = %s AND personId = %s"
            cursor.execute(query, (status, personId))
            existing_device = cursor.fetchone()

            if existing_device:
                return {'message': 'ColorBrightness entry already exists.'}, 400

            # 색상 및 밝기 등록
            query = "INSERT INTO color_brightness (color, brightness, status, personId) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (color, brightness, status, personId))
            color_brightness_id = cursor.lastrowid
            db.commit()

            return {
                'message': 'Color and brightness registered successfully',
                'colorBrightnessId': color_brightness_id
            }, 200
        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500


@color_brightness_ns.route('/<int:personId>')
class GetResource(Resource):
    def get(self, personId):
        """
        색상 및 밝기 조회
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
            # 색상 및 밝기 조회
            query = "SELECT * FROM color_brightness WHERE personId = %s"
            cursor.execute(query, (personId,))
            color_brightness = cursor.fetchall()

            return {'colorBrightness': color_brightness}, 200
        except Exception as e:
            return {'message': str(e)}, 500
        finally:
            cursor.close()
            db.close()


@color_brightness_ns.route('/<int:personId>/<string:status>')
class GetResource(Resource):
    def get(self, personId, status):
        """
        색상 및 밝기 Id 가져오기
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
            # 색상 및 밝기 Id 가져오기
            query = "SELECT * FROM color_brightness WHERE personId = %s AND status = %s"
            cursor.execute(query, (personId, status))
            color_brightness = cursor.fetchall()

            return {'colorBrightness': color_brightness}, 200
        except Exception as e:
            return {'message': str(e)}, 500
        finally:
            cursor.close()
            db.close()


@color_brightness_ns.route('/update/<int:colorBrightnessId>')
class UpdateResource(Resource):
    def put(self, colorBrightnessId):
        """
        색상 및 밝기 수정
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400

        data = request.json
        required_keys = ['color', 'brightness', 'status', 'personId']

        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        color = data['color']
        brightness = data['brightness']
        status = data['status']
        personId = data['personId']

        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()

        try:
            # 기존 데이터를 업데이트하는 쿼리
            query = """
                UPDATE color_brightness 
                SET color = %s, brightness = %s, status = %s, personId = %s 
                WHERE id = %s
            """
            cursor.execute(query, (color, brightness, status, personId, colorBrightnessId))

            # 데이터베이스 커밋
            db.commit()

            if cursor.rowcount == 0:
                # 업데이트된 행이 없으면, 존재하지 않는 ID에 대한 요청임
                return {'message': 'ColorBrightness entry not found.'}, 404

            return {
                'message': 'Color and brightness updated successfully',
                'colorBrightnessId': colorBrightnessId
            }, 200

        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500

        finally:
            cursor.close()
            db.close()
