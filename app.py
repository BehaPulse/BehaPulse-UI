# Flask Import
import json
from datetime import timedelta

from flask import Flask, session, request, jsonify
import requests
from flask_restx import Api, Resource, reqparse, Namespace
from flask_cors import CORS
import warnings
warnings.filterwarnings(action='ignore')

# Namespace Import
from API import *

# Dash Import
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from templates.page.app import admin_app


# 데이터베이스 설정을 파일에서 불러옵니다.
with open('config/server.json', 'r') as f:
    server = json.load(f)


app = Flask(__name__)
CORS(app)  # To handle CORS issues between Flask and Dash

app.secret_key = "BehaPulse"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)  # 세션 유지 시간을 30분으로 설정

api = Api(app, version='1.0', title='API Document', description='Check the REST API specification.', doc='/doc/')
admin_app.init_app(app)

# API에 네임스페이스 추가
api.add_namespace(user_ns)
api.add_namespace(device_ns)
api.add_namespace(user_device_ns)
api.add_namespace(dashboard_ns)
api.add_namespace(user_dashboard_ns)
api.add_namespace(user_dashboard_device_ns)
api.add_namespace(color_brightness_ns)
api.add_namespace(sensitivity_ns)
api.add_namespace(state_inference_ns)

# SmartThings 인증 관련(Valid Domain-SmartApp)
@app.route('/beha-pulse/main/more', methods=['POST'])
def get_request_details():
    headers = dict(request.headers)
    print("Headers:", headers)
    body = request.get_data(as_text=True)
    print("Body:", body)

    body = request.get_json()
    print("SmartThings Request body:", body)

    if body.get('lifecycle') == 'CONFIRMATION':
        confirmation_url = body['confirmationData']['confirmationUrl']
        
        try:
            # SmartThings에 GET 요청 보내기
            response = requests.get(confirmation_url)
            response.raise_for_status()  # 요청이 성공했는지 확인
            print(response.raise_for_status())
            return jsonify({'message': 'CONFIRMATION success'}), 200
        except requests.exceptions.RequestException as e:
            print(f'Error confirming SmartThings registration: {e}')
            return jsonify({'message': 'CONFIRMATION failed'}), 500
    else:
        return jsonify({'message': 'Not a confirmation request'}), 200

if __name__ == '__main__':
    # app.run(host=server['server']['host'], port=server['server']['port'])
    app.run(host=server['server']['bind-host'], port=server['server']['port'], ssl_context=(server['server']['ssl-cert-pem'], server['server']['ssl-key-pem']))

