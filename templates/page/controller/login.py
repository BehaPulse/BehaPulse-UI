from app import admin_app
from flask import Flask, session
from dash import Dash, dcc, html, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import requests
import json

with open('config/server.json', 'r') as f:
    server = json.load(f)

# 로그인 콜백 함수 정의
def login_controller(app):
    # 서버 사이드 콜백: 로그인 버튼 클릭 시 인증 처리
    @app.callback(
        [Output('login-result-store', 'data', allow_duplicate=True),  # 로그인 결과를 저장할 Store
         Output('login', 'href')],  # 페이지 이동을 처리할 dcc.Location
        [Input('login-button', 'n_clicks')],  # 로그인 버튼 클릭 감지
        [State('login-email', 'value'),  # 입력된 ID 값
         State('login-password', 'value')],  # 입력된 비밀번호 값
        prevent_initial_call=True
    )
    def authenticate_user(n_clicks, login_id, login_password):
        # 로그인 버튼이 클릭되지 않았거나, ID와 비밀번호가 입력되지 않았을 때
        if n_clicks:
            if not login_id or not login_password:
                return [{'success': False, 'message': '로그인 정보를 입력해주세요.'}, None]
            else:
                # 로그인 인증 요청
                api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/user/login'
                try:
                    response = requests.post(
                        api_url,
                        json={'userEmail': login_id, 'userPassword': login_password},
                        verify=server["server"]["verify"]
                    )

                    # 로그인 성공 시 메인 페이지로 리디렉션
                    if response.status_code == 200:
                        session['login'] = True  # 로그인 성공
                        session['user_id'] = login_id  # 사용자 ID 저장
                        session['user_name'] = response.json().get('userName')  # 사용자 이름 저장
                        return [{'success': True, 'message': '로그인 성공!'}, '/beha-pulse/main/']  # 메인 페이지 경로로 이동

                    # 로그인 실패 시
                    else:
                        return [{'success': False, 'message': '로그인에 실패했습니다. 아이디와 비밀번호를 확인해주세요.'}, '/beha-pulse/login/']
                except Exception as e:
                    return [{'success': False, 'message': f'서버 오류: {str(e)}'}, '/beha-pulse/login/']
        else:
            return [None, None]

    # 클라이언트 사이드 콜백: 로그인 결과가 업데이트될 때 alert 표시
    app.clientside_callback(
        """
        function(login_result) {
            if (login_result && login_result['success'] === false) {
                alert(login_result['message']);
            }
            return '';
        }
        """,
        Output('dummy-output', 'children', allow_duplicate=True),  # 결과를 출력할 dummy output
        [Input('login-result-store', 'data')]  # 로그인 결과가 변경될 때마다 트리거
        , prevent_initial_call=True
    )
