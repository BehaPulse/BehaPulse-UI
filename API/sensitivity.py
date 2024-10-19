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
    
sensitivity_ns = Namespace('sensitivity', description='Sensitivity API', doc='/sensitivity', path='/sensitivity')
sensitivity_field = sensitivity_ns.model('SensitivityModel', sensitivity_model)

@sensitivity_ns.route('/register')
class RegisterResource(Resource):
    @sensitivity_ns.expect(sensitivity_field, validate=True)
    def post(self):
        """
        민감도 등록
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400
        data = request.json
        required_keys = ['userEmail', 'targetStatus', 'weight']
        
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400
        
        user_email = data['userEmail']
        target_status = data['targetStatus']
        weight = data['weight']
        
        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        
        cursor = db.cursor()
        try:
            # 민감도 중복 확인
            query = "SELECT * FROM sensitivity WHERE userEmail = %s AND targetStatus = %s"
            cursor.execute(query, (user_email, target_status))
            existing_sensitivity = cursor.fetchone()
            
            if existing_sensitivity:
                return {'message': 'Sensitivity entry already exists.'}, 400
            
            # 민감도 등록
            query = "INSERT INTO sensitivity (userEmail, targetStatus, weight) VALUES (%s, %s, %s)"
            cursor.execute(query, (user_email, target_status, weight))
            sensitivity_id = cursor.lastrowid
            db.commit()
            
            return {'message': 'Sensitivity registered successfully.', 'sensitivityId': sensitivity_id}, 201
        except Exception as e:
            return {'message': 'Error occurred while registering sensitivity.', 'error': str(e)}, 500
        finally:
            cursor.close()
            db.close()
            
@sensitivity_ns.route('/<string:user_email>')
class GetResource(Resource):
    def get(self, user_email):
        """
        사용자의 민감도 조회
        """
        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor()
        
        try :
            query = "SELECT * FROM sensitivity WHERE userEmail = %s"
            cursor.execute(query, (user_email,))
            sensitivities = cursor.fetchall()
            
            if not sensitivities:
                return {'message': 'No sensitivity data found.'}, 404
            
            sensitivity_list = []
            for sensitivity in sensitivities:
                sensitivity_dict = {
                    'sensitivityId': sensitivity[0],
                    'userEmail': sensitivity[1],
                    'targetStatus': sensitivity[2],
                    'weight': float(sensitivity[3])
                }
                sensitivity_list.append(sensitivity_dict)
                
            return {'sensitivityList': sensitivity_list}, 200
        except Exception as e:
            return {'message': 'Error occurred while fetching sensitivity data.', 'error': str(e)}, 500
        finally:
            cursor.close()
            db.close()

@sensitivity_ns.route('/update/<string:user_email>/<string:target_status>')
class UpdateResource(Resource):
    @sensitivity_ns.expect(sensitivity_field, validate=True)
    def put(self, user_email, target_status):
        """
        민감도 수정
        """
        if not request.is_json:
            return {'message': 'Missing JSON in request'}, 400
        data = request.json
        required_keys = ['weight']
        
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400
        
        weight = data['weight']
        
        db = mysql.connector.connect(
            host=db_config['Database']['host'],
            user=db_config['Database']['user'],
            password=db_config['Database']['password'],
            database=db_config['Database']['database'],
            auth_plugin='mysql_native_password'
        )
        
        cursor = db.cursor()
        try:
            # 민감도 수정
            query = "UPDATE sensitivity SET weight = %s WHERE userEmail = %s AND targetStatus = %s"
            cursor.execute(query, (weight, user_email, target_status))
            db.commit()
            
            # 민감도가 동일하다면 수정하지 않음
            if cursor.rowcount == 0:
                return {'message': 'Sensitivity entry not found.'}, 404
            
            return {'message': 'Sensitivity updated successfully.'}, 200
        
            
        except Exception as e:
            return {'message': 'Error occurred while updating sensitivity.', 'error': str(e)}, 500
        finally:
            cursor.close()
            db.close()
    