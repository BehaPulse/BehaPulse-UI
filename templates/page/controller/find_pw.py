from app import admin_app
from flask import Flask, session
from dash import Dash, dcc, html, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import requests
from dash import Dash, dcc, html, callback_context, no_update
import json

from ..layout.find_pw import *

with open('config/server.json', 'r') as f:
    server = json.load(f)

def find_pw_controller(app):
    # 현재 단계에 따른 UI 업데이트
    @app.callback(
        [Output('find-pw-text-content', 'children'),
         Output('find-pw-main-content', 'children')],
        [Input('find-pw-current-step-store', 'data')],
    )
    def update_ui(step):
        return get_step_content(step)

    app.clientside_callback(
        """
        function(n_clicks, step, find_pw_data) {
            console.log("Current step:", step);
            console.log("Find PW data:", find_pw_data);
            
            const MAX_STEP = 4;  // 최대 단계 설정

            if (!n_clicks || step >= MAX_STEP) {
                return [find_pw_data, step];  // n_clicks가 없거나 최대 단계에 도달하면 현재 단계 유지
            }

            // Step에 따라 입력 필드에서 값 가져오기
            let idInput = document.getElementById('find-pw-input-id');
            
            let securityQuestionInput = document.getElementById('find-pw-input-security-question');
            let securityAnswerInput = document.getElementById('find-pw-input-security-answer')

            if (!find_pw_data) {
                find_pw_data = {};
            }

            // 단계별로 데이터를 저장하고 검사 후 버튼 상태 변경
            if (step === 1 && idInput) {
                find_pw_data['id'] = idInput.value;                
                if (!find_pw_data['id']) {
                    alert('아이디를 입력해주세요.');
                    return [find_pw_data, step];
                }
                console.log("ID stored: " + find_pw_data['id']);
            }
            if (step === 2 && securityQuestionInput && securityAnswerInput) {
          
                find_pw_data['securityQuestion'] = securityQuestionInput.value;
                find_pw_data['securityAnswer'] = securityAnswerInput.value;
                
                if (!find_pw_data['securityQuestion']) {
                    alert('질문을 입력해주세요.');
                    return [find_pw_data, step];
                }
                
                if (!find_pw_data['securityAnswer']) {
                    alert('답변을 입력해주세요.');
                    return [find_pw_data, step];
                }
                console.log("Question stored: " + find_pw_data['securityQuestion']);
                console.log("Answer stored: " + find_pw_data['securityAnswer']);
            }

            console.log("Updated find_pw_data data:", find_pw_data);
            return [find_pw_data, step < MAX_STEP ? step + 1 : step];
        }
        """,
        [Output('find-pw-data-store', 'data'),
         Output('find-pw-current-step-store', 'data')],
        [Input('find-pw-next-button', 'n_clicks')],
        [State('find-pw-current-step-store', 'data'),
         State('find-pw-data-store', 'data')],
        prevent_initial_call=True
    )

    @app.callback(
        [Output('find-pw-current-step-store', 'data', allow_duplicate=True),
         Output('find-pw', 'href')],
        [Input('find-pw-back-button', 'n_clicks')],
        [State('find-pw-current-step-store', 'data')],
        prevent_initial_call=True
    )
    def handle_back_button(n_clicks, current_step):
        if current_step == 1:
            return current_step, "/beha-pulse/login/"  # 첫 페이지에서는 /beha-pulse/로 이동
        elif current_step == 4:
            return 1, "/beha-pulse/login/"  # 마지막 페이지에서는 /beha-pulse/로 이동
        elif current_step == 5:
            return 1, "/beha-pulse/find_pw/"  # 오류 페이지에서는 /beha-pulse/find_pw/로 이동
        elif current_step == 6:
            return 1, "/beha-pulse/signup/"  # 회원 가입 페이지로 이동
        else:
            return current_step - 1, None  # 이전 단계로 이동

    @app.callback(
        [Output('find-pw-data-store', 'data', allow_duplicate=True),
         Output('find-pw-current-step-store', 'data', allow_duplicate=True)],
        [Input('find-pw-next-button', 'n_clicks')],
        [State('find-pw-data-store', 'data'),
         State('find-pw-current-step-store', 'data')]
        , prevent_initial_call=True
    )
    def get_input_value(n_clicks, find_pw_data, step):
        if step == 1 and n_clicks:
            required_fields = ['id']
            if not all([find_pw_data.get(key) for key in required_fields]):
                return find_pw_data, 5

            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/user/find_password/{find_pw_data["id"]}'

            try:
                response = requests.get(api_url, verify=server["server"]["verify"])

                if response.status_code == 200:
                    response = response.json()
                    find_pw_data['securityQuestion'] = response['securityQuestion']

                    return find_pw_data, no_update

                elif response.status_code == 404:
                    return find_pw_data, 6

            except requests.exceptions.RequestException as e:
                return find_pw_data, 5

        if step == 2 and n_clicks:
            required_fields = ['id', 'securityQuestion', 'securityAnswer']
            if not all([find_pw_data.get(key) for key in required_fields]):
                return find_pw_data, 5

            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/user/find_password/{find_pw_data["id"]}'
            json = {
                'securityQuestion': find_pw_data['securityQuestion'],
                'securityAnswer': find_pw_data['securityAnswer']
            }

            try:
                response = requests.post(api_url, json=json, verify=server["server"]["verify"])
                if response.status_code == 200:
                    response = response.json()
                    find_pw_data['tempPassword'] = response['temporaryPassword']

                    return find_pw_data, no_update
                elif response.status_code == 404:
                    return find_pw_data, 6
                else:
                    return find_pw_data, 5
            except requests.exceptions.RequestException as e:
                return find_pw_data, 5
        else:
            return no_update, no_update

    @app.callback(
        Output('find-pw-input-security-question', 'value'),
        [Input('find-pw-data-store', 'data')],
        prevent_initial_call=True
    )
    def update_security_question(find_pw_data):
        return find_pw_data.get('securityQuestion', '')

    @app.callback(
        [Output('find-pw-next-button', 'children'),
         Output('find-pw-next-button', 'href'), ],
        [Input('find-pw-current-step-store', 'data')]
    )
    def update_next_button_text(current_step):
        if current_step == 4:
            return "로그인", '/beha-pulse/login/'
        elif current_step == 6:
            return "회원 가입", '/beha-pulse/signup/'
        elif current_step == 5:
            return "돌아가기", '/beha-pulse/login/'
        else:
            return "다음", None

    @app.callback(
        Output('find-pw-temp-password', 'value'),
        [Input('find-pw-data-store', 'data')]
        , prevent_initial_call=True
    )
    def update_temp_password(find_pw_data):
        return find_pw_data.get('tempPassword', '')
