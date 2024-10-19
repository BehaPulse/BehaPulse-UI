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

state_inference_ns = Namespace('state_inference', description='State Inference API', doc='/state_inference',
                               path='/state_inference')
state_inference_field = state_inference_ns.model('StateInferenceModel', state_inference_model)


@state_inference_ns.route('/register')
class StateInferenceRegister(Resource):
    @state_inference_ns.expect(state_inference_field, validate=True)
    def post(self):
        """
        추론 결과 저장
        """

        if not request.json:
            return {'message': 'No input data provided'}, 400

        data = request.json

        required_fields = ['personId', 'inferenceTime', 'inferencedStatus']
        if not all([field in data for field in required_fields]):
            return {'message': 'Required fields are missing'}, 400

        person_id = data['personId']
        inference_time = data['inferenceTime']
        inferenced_status = data['inferencedStatus']

        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()

        try:
            query = "INSERT INTO state_inference (personId, inferenceTime, inferencedStatus) VALUES (%s, %s, %s)"
            cursor.execute(query, (person_id, inference_time, inferenced_status))
            db.commit()
            return {'message': 'state_inference registered successfully'}, 201


        except Exception as e:
            db.rollback()
            return {'message': str(e)}, 500

        finally:
            cursor.close()
            db.close()


@state_inference_ns.route('/list/<int:person_id>')
class GetPersonStateInference(Resource):
    def get(self, person_id):
        """
        사용자의 추론 결과 조회
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
            query = "SELECT * FROM state_inference WHERE personId = %s"
            cursor.execute(query, (person_id,))
            results = cursor.fetchall()

            if not results:
                return {'message': 'No state_inference data found'}, 404

            # 딕셔너리 목록을 반환하여 간소화
            return {'state_inference': [
                {
                    'inferencedStatus': result['inferencedStatus'],
                    'inferenceTime': result['inferenceTime'].strftime('%Y-%m-%d %H:%M:%S'),
                    'personId': result['personId'],
                }
                for result in results
            ]}, 200

        except Exception as e:
            return {'message': str(e)}, 500

        finally:
            cursor.close()
            db.close()


@state_inference_ns.route('/list/<int:person_id>/<string:date>')
class GetPersonStateInference(Resource):
    def get(self, person_id, date):
        """
        사용자의 추론 결과 조회 (년월일이 동일한 경우 필터링)
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
            # 정확한 날짜를 필터링 (년-월-일)
            query = """
                SELECT * FROM state_inference 
                WHERE personId = %s AND DATE(inferenceTime) = %s
            """
            cursor.execute(query, (person_id, date))
            results = cursor.fetchall()

            if not results:
                return {'message': 'No state_inference data found for the specified date'}, 404

            # 결과 목록을 반환 (간소화된 딕셔너리 형식)
            return {'state_inference': [
                {
                    'inferencedStatus': result['inferencedStatus'],
                    'inferenceTime': result['inferenceTime'].strftime('%Y-%m-%d %H:%M:%S'),
                    'personId': result['personId'],
                }
                for result in results
            ]}, 200

        except Exception as e:
            return {'message': str(e)}, 500

        finally:
            cursor.close()
            db.close()


