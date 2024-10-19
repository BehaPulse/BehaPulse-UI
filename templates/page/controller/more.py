from dash.exceptions import PreventUpdate

from app import admin_app
from flask import Flask, session
from dash import Dash, dcc, html, callback_context, no_update
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
import requests
import json
from datetime import datetime

from ..layout.content.more.more_help import get_step_content
from ..layout.content.more.more_password import get_step_content_more_password

import hashlib
import base64
import os
import random
import urllib.parse as urlparse
from urllib.parse import urlencode, quote
from requests.auth import HTTPBasicAuth
from urllib.parse import parse_qs, urlparse
import os

with open('config/server.json', 'r') as f:
    server = json.load(f)


def more_controller(app):
    @app.callback(
        Output('more', 'pathname'),
        [Input({'type': 'more-item', 'index': '개인정보 방침 조항'}, 'n_clicks'),
         Input('url', 'pathname')],
        prevent_initial_call=True
    )
    def redirect_to_privacy_policy(n_clicks, pathname):
        if n_clicks:
            return '/beha-pulse/main/more/privacy-policy/'
        return pathname

    @app.callback(
        Output('more', 'pathname', allow_duplicate=True),
        [Input({'type': 'more-item', 'index': '이용약관'}, 'n_clicks'),
         Input('url', 'pathname')],
        prevent_initial_call=True
    )
    def redirect_to_document(n_clicks, pathname):
        if n_clicks:
            return '/beha-pulse/main/more/document/'
        return pathname

    @app.callback(
        Output('more', 'pathname', allow_duplicate=True),
        [Input({'type': 'more-item', 'index': '앱 정보'}, 'n_clicks'),
         Input('url', 'pathname')],
        prevent_initial_call=True
    )
    def redirect_to_information(n_clicks, pathname):
        if n_clicks:
            return '/beha-pulse/main/more/information/'
        return pathname

    @app.callback(
        Output('more', 'pathname', allow_duplicate=True),
        [Input({'type': 'more-item', 'index': '도움말'}, 'n_clicks'),
         Input('url', 'pathname')],
        prevent_initial_call=True
    )
    def redirect_to_help(n_clicks, pathname):
        if n_clicks:
            return '/beha-pulse/main/more/help/'
        return pathname

    @app.callback(
        Output('more', 'pathname', allow_duplicate=True),
        [Input({'type': 'more-item', 'index': 'SmartThings 설정'}, 'n_clicks'),
         Input('url', 'pathname')],
        prevent_initial_call=True
    )
    def redirect_to_help(n_clicks, pathname):
        if n_clicks:
            return '/beha-pulse/main/more/smart-things/'
        return pathname

    @app.callback(
        Output('more', 'pathname', allow_duplicate=True),
        [Input({'type': 'more-item', 'index': '비밀번호 변경'}, 'n_clicks'),
         Input('url', 'pathname')],
        prevent_initial_call=True
    )
    def redirect_to_password(n_clicks, pathname):
        if n_clicks:
            return '/beha-pulse/main/more/password/'
        return pathname

    @app.callback(
        Output('more', 'pathname', allow_duplicate=True),
        [Input({'type': 'more-item', 'index': '동작 민감도 설정'}, 'n_clicks'),
         Input('url', 'pathname')],
        prevent_initial_call=True
    )
    def redirect_to_sensitivity(n_clicks, pathname):
        if n_clicks:
            return '/beha-pulse/main/more/sensitivity/'
        return pathname

    # base_oauth_url = 'https://api.smartthings.com/oauth'

    # verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
    # code_challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode('utf-8')).digest()).rstrip(b'=').decode('utf-8')
    # scopes = ['r:devices:*', 'w:devices:*', 'x:devices:*', 'r:hubs:*', 'r:locations:*', 'w:locations:*', 'x:locations:*', 'r:scenes:*', 'x:scenes:*', 'r:rules:*', 'w:rules:*']

    # login_failed = False
    # authentication_info = None
    # finish_url = f'{server["server"]["protocol"]}://{server["smartthings"]["redirect-host"]}' + '/beha-pulse/main/more' # Callback URL

    # # Define the necessary variables
    # client_id = server["smartthings"]['CLIENT_ID'] # OAuth Client Id
    # client_secret = server["smartthings"]['CLIENT_SECRET'] # OAuth Client Secret
    # redirect_uri = finish_url

    # @app.callback(
    #     Output({'type': 'more-item', 'index': 'SmartThings 설정'}, 'children', allow_duplicate=True),
    #     [Input('url', 'href')],  # URL of current page
    #     prevent_initial_call='initial_duplicate'
    # )
    # def extract_access_token(href):
    #     print('extract access token func called')
    #     if href is None:
    #         print('href is none', href)
    #         return "No URL provided."
    #     print(href)
    #     # Parse code from Query String - URL의 쿼리 스트링에서 파라미터 분석
    #     parsed_url = urlparse(href)
    #     query_params = parse_qs(parsed_url.query)

    #     # if 'code' parameter exists, parse that
    #     code_received = query_params.get('code', [None])[0]
    #     # access_token = session['access_token']
    #     if code_received:
    #         print('code_received', code_received)
    #         # Prepare the request URL and headers
    #         url = "https://api.smartthings.com/oauth/token"
    #         headers = {
    #             'Content-Type': 'application/x-www-form-urlencoded'
    #         }

    #         # Prepare the payload
    #         data = {
    #             'grant_type': 'authorization_code',
    #             'client_id': client_id,
    #             'code': code_received,
    #             'redirect_uri': redirect_uri
    #         }

    #         # Make the POST request
    #         response = requests.post(url, headers=headers, data=data, auth=HTTPBasicAuth(client_id, client_secret), timeout=10)

    #         # Check the response
    #         if response.status_code == 200:
    #             token_data = response.json()
    #             access_token = token_data.get('access_token')
    #             refresh_token = token_data.get('refresh_token')
    #             print(f"Access Token: {access_token}")
    #             print(f"Refresh Token: {refresh_token}")
    #             if access_token:
    #                 session['access_token'] = access_token
    #                 session['refresh_token'] = refresh_token
    #                 # Store token in DBMS through API CALL
    #                 api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/user/set_st_token/{session["user_id"]}'
    #                 data = {
    #                     "stAccessToken": access_token,
    #                     "stRefreshToken": refresh_token,
    #                 }
    #                 try:
    #                     response = requests.post(api_url, json=data, verify=server["server"]["verify"])
    #                     if response.status_code == 201:
    #                         return f"Access Token: {access_token}, and Refresh Token: {refresh_token}"
    #                     elif response.status_code == 404:
    #                         return "계정을 찾을 수 없습니다."
    #                     else:
    #                         return "서버 연결 실패"

    #                 except requests.exceptions.RequestException as e:
    #                     return f"An error occurred: {str(e)}"

    #                 # return f"Access Token: {access_token}, and Refresh Token: {refresh_token}"
    #             else:
    #                 return "Access Token not found in URL."
    #         else:
    #             print(f"Failed to obtain access token: {response.status_code}, {response.text}")
    #             return f"Failed to obtain access token: {response.status_code}, {response.text}"
    #     else:
    #         return ' '

    @app.callback(
        Output('more-smart-things-content', 'children'),
        Input('url', 'pathname')
    )
    def update_token_output(pathname):
        # authorize_url = f'{base_oauth_url}/authorize'
        # params = {
        #     'scope': '+'.join(scopes),
        #     'response_type': 'code',
        #     'client_id': client_id,
        #     'redirect_uri': finish_url,
        # }
        # authorize_url = f"{authorize_url}?{urlencode(params)}"
        # authorize_url = authorize_url.replace('%2B', '+')
        if pathname == '/beha-pulse/main/more/smart-things/':
            authorize_url = 'https://smart.musicnjoy.art/start_chal?userId=' + session['user_id']
            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/user/st_token/{session["user_id"]}'
            try:
                response = requests.get(api_url, verify=server["server"]["verify"])
                print(response.json())

                if response.status_code == 200:
                    res = response.json()['user']
                    access_token = res['stAccessToken']
                    refresh_token = res['stRefreshToken']
                    if access_token != None and refresh_token != None:
                            st_url = 'https://api.smartthings.com/v1/devices'
                            st_headers = {
                                'Authorization': f'Bearer {access_token}',
                                'Content-Type': 'application/json'
                            }
                            
                            st_response = requests.get(st_url, headers=st_headers)
                            print(st_response.status_code)
                            if st_response.status_code == 200:
                                return html.A('삼성 계정 연동 완료. 클릭시 재연동 시도.', href=authorize_url)
                            else:
                                return html.A('클릭해서 삼성 계정을 연동하세요.', href=authorize_url)
                    else:
                        print(response.status_code, response.text)
                        return html.A('클릭해서 삼성 계정을 연동하세요.', href=authorize_url)
                else:
                    print(response.status_code, response.text)
                    return html.A('클릭해서 삼성 계정을 연동하세요.', href=authorize_url)
            except Exception as e:
                print(str(e))
                return html.A('클릭해서 삼성 계정을 연동하세요.', href=authorize_url)

    @app.callback(
        [Output('more-overlay-background', 'style', allow_duplicate=True),
         Output('more-overlay-container', 'style', allow_duplicate=True)],
        [Input({'type': 'more-item', 'index': '로그아웃'}, 'n_clicks'),
         Input('more-overlay-background', 'n_clicks'),
         ],
        [State('more-overlay-background', 'style'),
         State('more-overlay-container', 'style')],
        prevent_initial_call=True
    )
    def loggout_overlay(n_clicks_button, n_clicks_background, background_style, container_style):
        ctx = callback_context
        if not ctx.triggered:
            return background_style, container_style

        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        # Triggered ID를 딕셔너리로 변환
        try:
            triggered_dict = json.loads(triggered_id)
        except json.JSONDecodeError:
            triggered_dict = {}

        # 로그아웃 버튼 클릭 시 오버레이 열기
        if triggered_dict.get('index') == '로그아웃' and triggered_dict.get('type') == 'more-item' and n_clicks_button:
            background_style['display'] = 'block'
            container_style['display'] = 'block'

        # 오버레이 클릭으로 닫기
        elif triggered_id == 'more-overlay-background' and n_clicks_background:
            background_style['display'] = 'none'
            container_style['display'] = 'none'

        return background_style, container_style

    @app.callback(
        [Output('more-overlay-background', 'style', allow_duplicate=True),
         Output('more-overlay-container', 'style', allow_duplicate=True),
         Input('more-cancel-button', 'n_clicks')],
        [State('more-overlay-background', 'style'),
         State('more-overlay-container', 'style')],
        prevent_initial_call=True
    )
    def cancel_delete(n_clicks, background_style, container_style):
        if n_clicks:
            background_style['display'] = 'none'
            container_style['display'] = 'none'
        return background_style, container_style

    @app.callback(
        [Output('more-id', 'children'),
         Output('more-name', 'children')],
        Input('url', 'pathname'),
    )
    def set_more_id(pathname):
        if pathname == '/beha-pulse/main/more/':
            return session['user_id'], session['user_name']

    # 로그아웃 구현
    @app.callback(
        Output('redirect', 'href', allow_duplicate=True),
        Input('more-confirm-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def logout(n_clicks):
        if n_clicks:
            session.clear()
            return '/beha-pulse/login/'
        return no_update

    @app.callback(
        Output('redirect', 'href', allow_duplicate=True),
        Input('more-back-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def back_to_more(n_clicks):
        if n_clicks:
            return '/beha-pulse/main/more/'
        return no_update

    @app.callback(
        Output('more-help-current-step-store', 'data'),
        Input('more-help-next-button', 'n_clicks'),
        State('more-help-current-step-store', 'data'),
        prevent_initial_call=True
    )
    def next_step(n_clicks, current_step):
        if n_clicks:
            return current_step + 1
        return current_step

    @app.callback(
        [Output('more-help-main-content', 'children'),
         Output('redirect', 'href', allow_duplicate=True)],
        Input('more-help-current-step-store', 'data'),
        prevent_initial_call=True
    )
    def update_step(step):
        if step <= 3:
            return get_step_content(step), no_update
        else:
            return '', '/beha-pulse/main/more/'

    @app.callback(
        [Output('more-password-text-content', 'children'),
         Output('more-password-main-content', 'children')],
        [Input('more-password-current-step-store', 'data')],
    )
    def update_ui(step):
        return get_step_content_more_password(step)

    # 비밀번호 일치 여부를 확인하는 callback 함수 정의
    @app.callback(
        [Output('password-check-icon', 'className', allow_duplicate=True),
         Output('password-check-icon-verify', 'className', allow_duplicate=True)],
        [Input('more-password-input-password', 'value'),
         Input('more-password-input-password-check', 'value')]
        , prevent_initial_call=True
    )
    def update_password_check_icon(password, confirm_password):
        # 비밀번호와 비밀번호 확인이 모두 입력되었을 때만 비교
        if password and confirm_password:
            if password == confirm_password:
                return 'ic-check w-20', 'ic-check w-20'  # 일치할 경우 체크 아이콘 표시
            else:
                return 'ic-x w-20', 'ic-x w-20'  # 일치하지 않을 경우 x 아이콘 표시
        else:
            # 비밀번호 입력 값이 하나라도 없으면 기본 x 아이콘 유지
            return 'ic-x w-20', 'ic-x w-20'

    # 2. 단계별 데이터 저장 및 다음 단계로 이동 콜백 (클라이언트 사이드 JavaScript 사용)
    app.clientside_callback(
        """
        function(n_clicks, step, password_data) {
            const MAX_STEP = 3;  // 최대 단계 설정

            if (!n_clicks || step >= MAX_STEP) {
                return [password_data, step];  // n_clicks가 없거나 최대 단계에 도달하면 현재 단계 유지
            }

            // Step에 따라 입력 필드에서 값 가져오기
            let oldPassword = document.getElementById('more-password-input-old-password');

            let passwordInput = document.getElementById('more-password-input-password');
            let passwordCheckInput = document.getElementById('more-password-input-password-check');

            if (!password_data) {
                password_data = {};
            }

            // 단계별로 데이터를 저장하고 검사 후 버튼 상태 변경
            if (step === 1 && oldPassword) {
                password_data['oldPassword'] = oldPassword.value;                
                if (!password_data['oldPassword']) {
                    alert('기존 비밀번호를 입력해주세요.');
                    return [password_data, step];
                }
                console.log("Name stored: " + password_data['oldPassword']);
            }
            
            else if (step === 2 && passwordInput && passwordCheckInput) {
                password_data['password'] = passwordInput.value;
                password_data['passwordCheck'] = passwordCheckInput.value;

                // 비밀번호와 비밀번호 확인 필드가 모두 존재하는지 확인
                if (!password_data['password'] || !password_data['passwordCheck']) {
                    alert('비밀번호와 비밀번호 확인을 모두 입력해 주세요.');
                    return [password_data, step];  // 값이 없으므로 현재 단계 유지
                }

                // 비밀번호와 비밀번호 확인이 일치하는지 확인
                if (password_data['password'] !== password_data['passwordCheck']) {
                    alert('비밀번호가 일치하지 않습니다. 다시 확인해 주세요.');

                    // 두 입력 필드의 값을 비움
                    passwordInput.value = '';
                    passwordCheckInput.value = '';

                    return [password_data, step];  // 값이 일치하지 않으므로 현재 단계 유지
                }

                console.log("Password stored: " + password_data['password']);
                console.log("PasswordCheck stored: " + password_data['passwordCheck']);
            }
            
            console.log("Updated password_data data:", password_data);
            return [password_data, step < MAX_STEP ? step + 1 : step];
        }
        """,
        [Output('more-password-data-store', 'data'),
         Output('more-password-current-step-store', 'data')],
        [Input('more-password-next-button', 'n_clicks')],
        [State('more-password-current-step-store', 'data'),
         State('more-password-data-store', 'data')]
    )

    # 콜백: 뒤로 가기 아이콘 클릭 시 단계 변경 또는 페이지 이동
    @app.callback(
        [Output('more-password-current-step-store', 'data', allow_duplicate=True),
         Output('more-password', 'href')],
        [Input('more-password-back-button', 'n_clicks')],
        [State('more-password-current-step-store', 'data')],
        prevent_initial_call=True
    )
    def handle_back_button(n_clicks, current_step):
        if current_step == 1 and n_clicks:
            return current_step, "/beha-pulse/main/more/"  # 첫 페이지에서는 /beha-pulse/로 이동
        elif current_step == 3 and n_clicks:
            session.clear()
            return 1, '/beha-pulse/login/'
        else:
            return current_step - 1, None  # 이전 단계로 이동

    @app.callback(
        [Output('more-password-next-button', 'children')],
        Input('more-password-next-button', 'n_clicks'),
        State('more-password-current-step-store', 'data'),
    )
    def update_next_button_text(n_clicks, current_step):
        if current_step == 2 and n_clicks:
            return ["재로그인"]
        else:
            return ["다음"]

    @app.callback(
        Output('redirect', 'href', allow_duplicate=True),
        Input('more-password-next-button', 'n_clicks'),
        [State('more-password-current-step-store', 'data'),
         State('more-password-next-button', 'children')],
        prevent_initial_call=True
    )
    def redirect_to_login(n_clicks, current_step, next_button_text):
        if current_step == 3 and n_clicks and next_button_text == "재로그인":
            session.clear()
            return '/beha-pulse/login/'
        return no_update

    @app.callback(
        [Output('more-password-current-step-store', 'data', allow_duplicate=True),
         [Output('more-password-next-button', 'children', allow_duplicate=True)],
         ],
        Input('more-password-next-button', 'n_clicks'),
        [State('more-password-current-step-store', 'data'),
         State('more-password-data-store', 'data')
         ],
        prevent_initial_call=True

    )
    def set_new_password(n_clicks, current_step, password_data):
        if n_clicks and current_step == 2:
            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/user/update/password/{session["user_id"]}'
            data = {
                'oldPassword': password_data['oldPassword'],
                'newPassword': password_data['password']
            }
            try:
                response = requests.put(api_url, json=data, verify=server["server"]["verify"])
                if response.status_code == 200:
                    return current_step + 1, ["재로그인"]
                else:
                    return current_step - 1, ["다음"]
            except requests.exceptions.RequestException as e:
                return 4, ["재로그인"]

        return no_update

    @app.callback(
        [Output('more-sensitivity-lying-slider', 'value'),
         Output('more-sensitivity-empty-slider', 'value'),
         Output('more-sensitivity-sitting-slider', 'value')],
        Input('url', 'pathname'),
    )
    def set_sensitivity_slider_value(pathname):
        lying, empty, sitting = 1, 1, 1
        if pathname == '/beha-pulse/main/more/sensitivity/':
            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/sensitivity/{session["user_id"]}'
            try:
                response = requests.get(api_url, verify=server["server"]["verify"])
                if response.status_code == 200:
                    sensitivities = response.json().get('sensitivityList')
                    for sensitivity in sensitivities:
                        if sensitivity['targetStatus'] == '누워있음':
                            lying = sensitivity['weight']
                        elif sensitivity['targetStatus'] == '비어있음':
                            empty = sensitivity['weight']
                        elif sensitivity['targetStatus'] == '앉아있음':
                            sitting = sensitivity['weight']
                    return lying, empty, sitting
                else:
                    return 1, 1, 1
            except requests.exceptions.RequestException as e:
                return 1, 1, 1
        return 1, 1, 1

    @app.callback(
        Output('redirect', 'href', allow_duplicate=True),
        Input('more-sensitivity-save-button', 'n_clicks'),
        [State('more-sensitivity-lying-slider', 'value'),
         State('more-sensitivity-empty-slider', 'value'),
         State('more-sensitivity-sitting-slider', 'value'),
         ],
        prevent_initial_call=True
    )
    # 민감도 저장
    # Case 1 : 민감도가 존재하지 않을 때
    #        a. 민감도를 저장
    # Case 2 : 민감도가 존재할 때
    #       a. 민감도가 변경되었을 때 변경된 민감도를 업데이트
    #       b. 민감도가 변경되지 않았을 때 변경하지 않음
    def save_weight(n_clicks, lying, empty, sitting):
        if n_clicks:
            new_sensitivities = {
                '누워있음': lying,
                '비어있음': empty,
                '앉아있음': sitting
            }
            # 존재 여부 확인
            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/sensitivity/{session["user_id"]}'
            try:
                response = requests.get(api_url, verify=server["server"]["verify"])
                if response.status_code == 200:
                    sensitivities = response.json().get('sensitivityList')
                    old_sensitivities = {}
                    for sensitivity in sensitivities:
                        old_sensitivities[sensitivity['targetStatus']] = sensitivity['weight']

                    api_count = 0
                    # 변경 사항 확인 및 업데이트 또는 등록 수행
                    for status in new_sensitivities:
                        new_weight = new_sensitivities[status]

                        if status not in old_sensitivities:
                            # Case 1: 민감도가 존재하지 않으면 새로 추가
                            add_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/sensitivity/register'
                            data = {
                                'userEmail': session["user_id"],
                                'targetStatus': status,
                                'weight': new_weight
                            }
                            add_response = requests.post(add_url, json=data, verify=server["server"]["verify"])

                        elif old_sensitivities[status] != new_weight:
                            # Case 2: 민감도가 존재하지만 값이 변경되었으면 업데이트
                            update_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/sensitivity/update/{session["user_id"]}/{status}'
                            data = {
                                'userEmail': session["user_id"],
                                'targetStatus': status,
                                'weight': new_weight
                            }

                            update_response = requests.put(update_url, json=data, verify=server["server"]["verify"])

                        api_count += 1

                    if api_count == len(new_sensitivities):
                        return '/beha-pulse/main/more/sensitivity/'

                # 존재하지 않음 바로 저장
                elif response.status_code == 404:
                    api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/sensitivity/register'
                    api_count = 0
                    for item in new_sensitivities:
                        data = {
                            'userEmail': session["user_id"],
                            'targetStatus': item,
                            'weight': new_sensitivities[item]
                        }
                        response = requests.post(api_url, json=data, verify=server["server"]["verify"])
                        if response.status_code == 201:
                            api_count += 1
                            if api_count == len(new_sensitivities):
                                return '/beha-pulse/main/more/sensitivity/'
                else:
                    return no_update
            except requests.exceptions.RequestException as e:
                # return 1, 1, 1
                return no_update
        return no_update
