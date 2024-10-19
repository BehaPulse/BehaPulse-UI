from app import admin_app
from flask import Flask, session
from dash import Dash, dcc, html, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import requests
from dash import Dash, dcc, html, callback_context, no_update
import json
from ..layout.signup import *

with open('config/server.json', 'r') as f:
    server = json.load(f)


def signup_controller(app):
    # 현재 단계에 따른 UI 업데이트
    @app.callback(
        [Output('signup-text-content', 'children'),
         Output('signup-main-content', 'children')],
        [Input('current-step-store', 'data')],
    )
    def update_ui(step):
        return get_step_content(step)

    # 2. 단계별 데이터 저장 및 다음 단계로 이동 콜백 (클라이언트 사이드 JavaScript 사용)
    app.clientside_callback(
        """
        function(n_clicks, step, signup_data) {
            const MAX_STEP = 7;  // 최대 단계 설정
            
            if (!n_clicks || step >= MAX_STEP) {
                return [signup_data, step];  // n_clicks가 없거나 최대 단계에 도달하면 현재 단계 유지
            }

            // Step에 따라 입력 필드에서 값 가져오기
            let nameInput = document.getElementById('sign-input-name');
            
            let manButton = document.getElementById('sign-input-gender-man');
            let womanButton = document.getElementById('sign-input-gender-woman');
            
            let yearInput = document.getElementById('sign-input-year');
            let monthInput = document.getElementById('sign-input-month');
            let dayInput = document.getElementById('sign-input-day');
            
            let idInput = document.getElementById('sign-input-id');
            
            let passwordInput = document.getElementById('sign-input-password');
            let passwordCheckInput = document.getElementById('sign-input-password-check');
            
            let securityQuestionInput = document.getElementById('sign-input-security-question');
            let securityAnswerInput = document.getElementById('sign-input-security-answer');
            
            
            if (!signup_data) {
                signup_data = {};
            }

            // 단계별로 데이터를 저장하고 검사 후 버튼 상태 변경
            if (step === 1 && nameInput) {
                signup_data['name'] = nameInput.value;                
                if (!signup_data['name']) {
                    alert('이름을 입력해주세요.');
                    return [signup_data, step];
                }
                console.log("Name stored: " + signup_data['name']);

            }
            else if (step === 2 && manButton && womanButton) {
                // 각 버튼의 상태를 직접 확인하여 성별 결정
                if (manButton.style.fontWeight === '900') {
                    signup_data['gender'] = 'male';
                } else if (womanButton.style.fontWeight === '900') {
                    signup_data['gender'] = 'female';
                }
                if (!signup_data['gender']) {
                    alert('성별을 선택해주세요.');
                    return [signup_data, step];
                }
                console.log("Gender stored: " + signup_data['gender']);

            }
            else if (step === 3 && yearInput && monthInput && dayInput) {
                // 입력값을 숫자로 변환
                signup_data['year'] = parseInt(yearInput.value, 10);
                signup_data['month'] = parseInt(monthInput.value, 10);
                signup_data['day'] = parseInt(dayInput.value, 10);
                
                // 값이 비어 있으면 경고
                if (!signup_data['year'] || !signup_data['month'] || !signup_data['day']) {
                    alert('생년월일을 입력해주세요.');
                    return [signup_data, step];
                }
            
                // 생년월일 유효성 검사
                if (signup_data['year'] < 1900 || signup_data['year'] > new Date().getFullYear()) {
                    alert('올바른 연도를 입력해주세요.');
                    yearInput.value = '';
                    return [signup_data, step];
                }
                if (signup_data['month'] < 1 || signup_data['month'] > 12) {
                    alert('올바른 월을 입력해주세요.');
                    monthInput.value = '';
                    return [signup_data, step];
                }
            
                // 각 달의 최대 일수 확인 함수
                function getDaysInMonth(year, month) {
                    return new Date(year, month, 0).getDate();  // 해당 월의 마지막 날짜 반환
                }
            
                // 입력된 월의 최대 일수 확인
                let maxDays = getDaysInMonth(signup_data['year'], signup_data['month']);
                if (signup_data['day'] < 1 || signup_data['day'] > maxDays) {
                    alert(`올바른 일을 입력해주세요. ${signup_data['month']}월은 ${maxDays}일까지 있습니다.`);
                    dayInput.value = '';
                    return [signup_data, step];
                }
            
                // 생년월일 입력 양식 확인 yyyy mm dd (한 자리수 월/일의 경우 0 추가)
                signup_data['month'] = signup_data['month'] < 10 ? '0' + signup_data['month'] : signup_data['month'].toString();
                signup_data['day'] = signup_data['day'] < 10 ? '0' + signup_data['day'] : signup_data['day'].toString();
            
                console.log("Year stored: " + signup_data['year']);
                console.log("Month stored: " + signup_data['month']);
                console.log("Day stored: " + signup_data['day']);
            }
            else if (step === 4 && idInput) {
                signup_data['id'] = idInput.value;
                
                if (!signup_data['id']) {
                    alert('아이디를 입력해주세요.');
                    return [signup_data, step];
                }
                
                // 중복 확인이 완료되지 않은 경우
                if (signup_data['id_validated'] === undefined || signup_data['id_validated'] === false) {
                    alert('아이디 중복 확인을 해주세요.');
                    return [signup_data, step];
                }
                
                console.log("ID stored: " + signup_data['id']);
            }
            else if (step === 5 && passwordInput && passwordCheckInput) {
                signup_data['password'] = passwordInput.value;
                signup_data['passwordCheck'] = passwordCheckInput.value;
                
                // 비밀번호와 비밀번호 확인 필드가 모두 존재하는지 확인
                if (!signup_data['password'] || !signup_data['passwordCheck']) {
                    alert('비밀번호와 비밀번호 확인을 모두 입력해 주세요.');
                    return [signup_data, step];  // 값이 없으므로 현재 단계 유지
                }
            
                // 비밀번호와 비밀번호 확인이 일치하는지 확인
                if (signup_data['password'] !== signup_data['passwordCheck']) {
                    alert('비밀번호가 일치하지 않습니다. 다시 확인해 주세요.');
                    
                    // 두 입력 필드의 값을 비움
                    passwordInput.value = '';
                    passwordCheckInput.value = '';
                    
                    return [signup_data, step];  // 값이 일치하지 않으므로 현재 단계 유지
                }
                
                console.log("Password stored: " + signup_data['password']);
                console.log("PasswordCheck stored: " + signup_data['passwordCheck']);
            }
            else if (step === 6 && securityQuestionInput && securityAnswerInput) {
                signup_data['securityQuestion'] = securityQuestionInput.value;
                signup_data['securityAnswer'] = securityAnswerInput.value;
                
                if (!signup_data['securityQuestion'] || !signup_data['securityAnswer']) {
                    alert('보안 질문과 답변을 모두 입력해 주세요.');
                    return [signup_data, step];  // 값이 없으므로 현재 단계 유지
                }
                signup_data['FinalStep'] = true;
                console.log("SecurityQuestion stored: " + signup_data['securityQuestion']);
                console.log("SecurityAnswer stored: " + signup_data['securityAnswer']);
            }
            
            console.log("Updated signup data:", signup_data);
            return [signup_data, step < MAX_STEP ? step + 1 : step];
        }
        """,
        [Output('signup-data-store', 'data'),
         Output('current-step-store', 'data')],
        [Input('signup-next-button', 'n_clicks')],
        [State('current-step-store', 'data'),
         State('signup-data-store', 'data')]
    )

    @app.callback(
        [Output('sign-input-gender-man', 'style'),
         Output('sign-input-gender-woman', 'style')],
        [Input('sign-input-gender-man', 'n_clicks'),
         Input('sign-input-gender-woman', 'n_clicks')]
    )
    def update_button_style(man_clicks, woman_clicks):
        # 기본 스타일 설정
        default_style = {'font-weight': 'normal'}
        active_style = {'font-weight': '900'}

        # 클릭 컨텍스트를 확인하여 누가 클릭되었는지 확인
        ctx = callback_context
        if not ctx.triggered:
            return default_style, default_style
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        # 버튼 ID에 따라 스타일 변경
        if button_id == 'sign-input-gender-man':
            return active_style, default_style
        elif button_id == 'sign-input-gender-woman':
            return default_style, active_style
        else:
            return default_style, default_style

    # 비밀번호 일치 여부를 확인하는 callback 함수 정의
    @app.callback(
        [Output('password-check-icon', 'className'),
         Output('password-check-icon-verify', 'className')],
        [Input('sign-input-password', 'value'),
         Input('sign-input-password-check', 'value')]
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

    # 콜백: 뒤로 가기 아이콘 클릭 시 단계 변경 또는 페이지 이동
    @app.callback(
        [Output('current-step-store', 'data', allow_duplicate=True),
         Output('signup', 'href')],
        [Input('signup-back-button', 'n_clicks')],
        [State('current-step-store', 'data')],
        prevent_initial_call=True
    )
    def handle_back_button(n_clicks, current_step):
        if current_step == 1:
            return current_step, "/beha-pulse/"  # 첫 페이지에서는 /beha-pulse/로 이동
        elif current_step == 8:
            return 1, "/beha-pulse/"
        else:
            return current_step - 1, None  # 이전 단계로 이동

    # 클라이언트 사이드 콜백: 이름을 최종 단계에서 표시
    app.clientside_callback(
        """
        function(step, signup_data) {
            if (step === 7 && signup_data && signup_data['name']) {
                return "환영합니다, " + signup_data['name'] + "님!";
            }
            return "";
        }
        """,
        Output('signup-final-name', 'children'),
        [Input('current-step-store', 'data')],
        [State('signup-data-store', 'data')]
    )

    # 현재 단계에 따라 signup-next-button의 텍스트를 동적으로 변경하는 콜백
    @app.callback(
        [Output('signup-next-button', 'children'),
         Output('signup-next-button', 'href')],
        [Input('current-step-store', 'data')]
    )
    def update_next_button_text(current_step):
        if current_step == 7:
            return "로그인", '/beha-pulse/login/'
        else:
            return "다음 단계", None

    # 아이디 중복 확인 콜백 (ID 중복 확인 결과를 signup-data-store에만 반영)
    @app.callback(
        Output('signup-data-store', 'data', allow_duplicate=True),  # signup_data 상태만 업데이트
        [Input('sign-duplicate-check-btn', 'n_clicks')],  # 중복 확인 버튼 클릭 이벤트 감지
        [State('sign-input-id', 'value'),  # 현재 입력된 ID 값
         State('signup-data-store', 'data')]  # 현재 signup_data 값
        , prevent_initial_call=True
    )
    def check_id(n_clicks, user_id, signup_data):
        # 기본값 설정
        if not signup_data:
            signup_data = {}

        if n_clicks:  # 중복 확인 버튼이 클릭된 경우에만 실행
            if not user_id:  # ID가 비어 있는 경우
                signup_data['id_validated'] = False
                return signup_data

            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/user/check-email/{user_id}'

            # ID 중복 확인 API 호출
            try:
                response = requests.get(api_url, verify=server["server"]["verify"])
                if response.status_code == 200:
                    # ID가 이미 존재할 경우
                    signup_data['id_validated'] = False  # 중복됨
                elif response.status_code == 404:
                    # ID가 존재하지 않을 경우
                    signup_data['id_validated'] = True  # 사용 가능
                else:
                    # 기타 상태 코드
                    signup_data['id_validated'] = False
            except requests.exceptions.RequestException:
                signup_data['id_validated'] = False
        return signup_data

    # ID 중복 확인 결과에 따라 버튼 색상 업데이트 콜백
    @app.callback(
        Output('sign-duplicate-check-btn', 'style'),  # 버튼의 스타일 업데이트
        [Input('signup-data-store', 'data')]  # signup_data 상태를 감지
    )
    def update_button_color(signup_data):
        # 기본 스타일 설정
        button_style = {'background-color': '#FF0000'}  # 기본 색상 (빨간색)

        # signup_data가 있는지 확인하고, 'id_validated' 값에 따라 색상 변경
        if signup_data and signup_data.get('id_validated'):
            button_style['background-color'] = '#00C443'  # ID가 사용 가능할 때 색상 변경 (녹색)

        return button_style

    @app.callback(
        Output('signup-data-store', 'data', allow_duplicate=True),
        [Input('sign-input-id', 'value')],
        [State('signup-data-store', 'data')]
        , prevent_initial_call=True
    )
    def reset_id_validation(user_id, signup_data):
        # signup_data가 비어 있을 경우 초기화
        if not signup_data:
            signup_data = {}

        # ID 입력이 변경되면 id_validated를 초기화 (False로 설정)
        signup_data['id_validated'] = False
        return signup_data

    # 새로운 회원가입 API 호출 콜백 추가
    @app.callback(
        [Output('signup-data-store', 'data', allow_duplicate=True),  # signup 데이터 업데이트
         Output('current-step-store', 'data', allow_duplicate=True)],  # 단계 업데이트
        [Input('signup-next-button', 'n_clicks')],  # Next 버튼 클릭 감지
        [State('signup-data-store', 'data'),  # 현재 입력된 데이터
         State('current-step-store', 'data')],  # 현재 단계
        prevent_initial_call=True
    )
    def signup(n_clicks, signup_data, step):
        # 단계 6에서 API 호출 실행
        if step == 6 and n_clicks and signup_data['FinalStep']:
            # 모든 필드가 존재하는지 확인
            required_fields = ['id', 'password', 'name', 'gender', 'year', 'month', 'day', 'securityQuestion',
                               'securityAnswer']
            if not all([signup_data.get(key) for key in required_fields]):
                return signup_data, 8  # 오류 단계로 설정

            # 생년월일 포맷 설정
            birth_date = f"{signup_data['year']}-{signup_data['month']}-{signup_data['day']}"

            # 회원가입 API 요청 데이터 생성
            payload = {
                "userEmail": signup_data['id'],
                "userPassword": signup_data['password'],
                "userName": signup_data['name'],
                "userGender": signup_data['gender'],
                "securityQuestion": signup_data['securityQuestion'],
                "securityAnswer": signup_data['securityAnswer'],
                "birthDate": birth_date
            }
            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/user/register'
            # 회원가입 API 요청
            try:
                response = requests.post(api_url, json=payload, verify=server["server"]["verify"])

                if response.status_code == 201:
                    # 회원가입 성공 시 step을 7로 설정
                    return signup_data, 7
                else:
                    # 회원가입 실패 시 오류 단계로 이동 (step = 8)
                    return signup_data, 8
            except requests.exceptions.RequestException as e:
                return signup_data, 8  # 오류 단계로 설정

        return no_update, no_update
