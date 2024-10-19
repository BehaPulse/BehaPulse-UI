from app import admin_app
from flask import Flask, session
from dash import Dash, dcc, html, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import requests
from dash import Dash, dcc, html, callback_context, no_update
import json
from ..layout.find_id import *

with open('config/server.json', 'r') as f:
    server = json.load(f)

def find_id_controller(app):
    # 현재 단계에 따른 UI 업데이트
    @app.callback(
        [Output('find-id-text-content', 'children'),
         Output('find-id-main-content', 'children')],
        [Input('find-id-current-step-store', 'data')],
    )
    def update_ui(step):
        return get_step_content(step)

    app.clientside_callback(
        """
        function(n_clicks, step, find_id_data) {
            console.log("Current step:", step);
            console.log("Find ID data:", find_id_data);
            
            const MAX_STEP = 3;  // 최대 단계 설정
            
            if (!n_clicks || step >= MAX_STEP) {
                return [find_id_data, step];  // n_clicks가 없거나 최대 단계에 도달하면 현재 단계 유지
            }

            // Step에 따라 입력 필드에서 값 가져오기
            let nameInput = document.getElementById('find-id-input-name');

            let yearInput = document.getElementById('find-id-input-year');
            let monthInput = document.getElementById('find-id-input-month');
            let dayInput = document.getElementById('find-id-input-day');

            if (!find_id_data) {
                find_id_data = {};
            }

            // 단계별로 데이터를 저장하고 검사 후 버튼 상태 변경
            if (step === 1 && nameInput) {
                find_id_data['name'] = nameInput.value;                
                if (!find_id_data['name']) {
                    alert('이름을 입력해주세요.');
                    return [find_id_data, step];
                }
                console.log("Name stored: " + find_id_data['name']);
            }
        
            else if (step === 2 && yearInput && monthInput && dayInput) {
                // 입력값을 숫자로 변환
                find_id_data['year'] = parseInt(yearInput.value, 10);
                find_id_data['month'] = parseInt(monthInput.value, 10);
                find_id_data['day'] = parseInt(dayInput.value, 10);

                // 값이 비어 있으면 경고
                if (!find_id_data['year'] || !find_id_data['month'] || !find_id_data['day']) {
                    alert('생년월일을 입력해주세요.');
                    return [find_id_data, step];
                }

                // 생년월일 유효성 검사
                if (find_id_data['year'] < 1900 || find_id_data['year'] > new Date().getFullYear()) {
                    alert('올바른 연도를 입력해주세요.');
                    yearInput.value = '';
                    return [find_id_data, step];
                }
                if (find_id_data['month'] < 1 || find_id_data['month'] > 12) {
                    alert('올바른 월을 입력해주세요.');
                    monthInput.value = '';
                    return [find_id_data, step];
                }

                // 각 달의 최대 일수 확인 함수
                function getDaysInMonth(year, month) {
                    return new Date(year, month, 0).getDate();  // 해당 월의 마지막 날짜 반환
                }

                // 입력된 월의 최대 일수 확인
                let maxDays = getDaysInMonth(find_id_data['year'], find_id_data['month']);
                if (find_id_data['day'] < 1 || find_id_data['day'] > maxDays) {
                    alert(`올바른 일을 입력해주세요. ${find_id_data['month']}월은 ${maxDays}일까지 있습니다.`);
                    dayInput.value = '';
                    return [find_id_data, step];
                }

                // 생년월일 입력 양식 확인 yyyy mm dd (한 자리수 월/일의 경우 0 추가)
                find_id_data['month'] = find_id_data['month'] < 10 ? '0' + find_id_data['month'] : find_id_data['month'].toString();
                find_id_data['day'] = find_id_data['day'] < 10 ? '0' + find_id_data['day'] : find_id_data['day'].toString();

                console.log("Year stored: " + find_id_data['year']);
                console.log("Month stored: " + find_id_data['month']);
                console.log("Day stored: " + find_id_data['day']);
            }
            
            console.log("Updated find_id data:", find_id_data);
            return [find_id_data, step < MAX_STEP ? step + 1 : step];
        }
        """,
        [Output('find-id-data-store', 'data'),
         Output('find-id-current-step-store', 'data')],
        [Input('find-id-next-button', 'n_clicks')],
        [State('find-id-current-step-store', 'data'),
         State('find-id-data-store', 'data')]
    )

    @app.callback(
        [Output('find-id-current-step-store', 'data', allow_duplicate=True),
         Output('find-id', 'href')],
        [Input('find-id-back-button', 'n_clicks')],
        [State('find-id-current-step-store', 'data')],
        prevent_initial_call=True
    )
    def handle_back_button(n_clicks, current_step):
        if current_step == 1:
            return current_step, "/beha-pulse/login/"  # 첫 페이지에서는 /beha-pulse/로 이동
        elif current_step == 3:
            return 1, "/beha-pulse/login/"  # 마지막 페이지에서는 /beha-pulse/로 이동
        else:
            return current_step - 1, None  # 이전 단계로 이동

    @app.callback(
        [Output('find-id-next-button', 'children'),
         Output('find-id-next-button', 'href')],
        [Input('find-id-current-step-store', 'data')]
    )
    def update_next_button_text(current_step):
        if current_step == 3:
            return "로그인", '/beha-pulse/login/'
        elif current_step == 5:
            return "회원 가입", '/beha-pulse/signup/'
        else:
            return "다음", None

    # 아이디 찾기 API 호출 콜백
    @app.callback(
        [Output('find-id-data-store', 'data', allow_duplicate=True),
         Output('find-id-current-step-store', 'data', allow_duplicate=True)],  # 단계 업데이트
        [Input('find-id-next-button', 'n_clicks')],  # Next 버튼 클릭 감지
        [State('find-id-data-store', 'data'),  # 현재 입력된 데이터
         State('find-id-current-step-store', 'data')],  # 현재 단계
        prevent_initial_call=True
    )
    def find_id(n_clicks, find_id_data, current_step):
        if current_step == 2 and n_clicks:
            # 필수 입력 필드 확인
            required_fields = ['name', 'year', 'month', 'day']
            if not all([find_id_data.get(key) for key in required_fields]):
                return find_id_data, 4  # 필수 입력 항목이 없을 때 오류 단계로 설정

            # 생년월일을 'YYYY-MM-DD' 형식으로 변환
            birth_date = f"{find_id_data['year']}-{find_id_data['month']}-{find_id_data['day']}"

            # API 요청 URL
            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/user/find_id/{find_id_data["name"]}/{birth_date}'

            try:
                # API 호출
                response = requests.get(api_url, verify=server["server"]["verify"])

                # 응답이 성공적일 때
                if response.status_code == 200:
                    response_data = response.json()
                    find_id_data['userEmails'] = response_data.get('userEmails', [])
                    return find_id_data, 3

                # 이메일이 존재하지 않을 때
                elif response.status_code == 404:
                    return find_id_data, 5

                # 기타 오류 응답 처리
                else:
                    return find_id_data, 4  # 오류 단계로 이동

            except requests.exceptions.RequestException:
                # 요청 실패 (네트워크 문제 또는 서버 오류 등)
                return find_id_data, 4  # 오류 단계로 이동

        # 현재 단계가 ID 찾기 단계가 아닐 때는 아무 작업도 하지 않음
        return no_update, no_update

    # 아이디 찾기 결과 표시 콜백
    @app.callback(
        [Output('find-final-name', 'children'),
         Output('find-final-id', 'children')],
        [Input('find-id-next-button', 'n_clicks')],  # Next 버튼 클릭 감지
        [State('find-id-current-step-store', 'data'),
         State('find-id-data-store', 'data')],
    )
    def display_find_id_result(n_clicks, current_step, find_id_data):
        if current_step == 3 and n_clicks:
            # 결과 표시
            id_text = ""
            if find_id_data.get('userEmails'):
                name_text = f'{find_id_data["name"]}님의 아이디는'
                for email in find_id_data['userEmails']:
                    if len(email) > 3:
                        # 마지막 3글자를 *로 대체
                        email = email[:-3] + '***'

                    id_text += f'{email}, '
                id_text = id_text[:-2] + ' 입니다.'
                return name_text, id_text
            else:
                return "", ""
        return "", ""
