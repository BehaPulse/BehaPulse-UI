from dash.exceptions import PreventUpdate

from app import admin_app
from flask import Flask, session
from dash import Dash, dcc, html, callback_context, no_update
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
import plotly.graph_objs as go

import requests
import json
from datetime import datetime

from ..layout.content.dashboard.dashboard import *
from ..layout.content.dashboard.dashboard_add import *
from ..layout.content.dashboard.dashboard_delete import *
from ..layout.content.dashboard.dashboard_not_connected import *

with open('config/server.json', 'r') as f:
    server = json.load(f)


def no_row_item(initial=True):
    if initial:
        src = '../../assets/img/error.svg'
    else:
        src = '../../../assets/img/error.svg'
    return html.Div([
        html.Img(src=src, style={'width': '15vh', 'height': '15vh'}),
        html.Span("등록된 사용자가 없습니다.", style={'font-weight': 'bold', 'font-size': '20px', 'margin-top': '20px'}),
    ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'height': '100%',
              'flex-direction': 'column'})


def dashboard_controller(app):
    # 현재 단계에 따른 UI 업데이트
    @app.callback(
        [Output('dashboard-add-text-content', 'children'),
         Output('dashboard-add-main-content', 'children')],
        [Input('dashboard-add-current-step-store', 'data')],
    )
    def update_ui(step):
        # set Default value
        step = step if step else 1

        return get_step_content(step)

    @app.callback(
        Output('dashboard-rows', 'children'),
        Input('url', 'pathname')
    )
    def set_dashboard_list_row(pathname):
        if pathname == '/beha-pulse/main/dashboard/':

            dashboard_row = []
            user_id = session.get('user_id')
            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/user_dashboard_device/user_dashboard_devices/{user_id}/{session["selected_location"]}'
            try:
                response = requests.get(api_url, verify=server["server"]["verify"])
                if response.status_code == 200:
                    # 디바이스가 설치된 위치의 personId 목록을 가져옴 그걸 바탕으로 다시 personId에 해당하는 정보를 가져옴
                    person_ids = response.json().get('user_dashboard_device', [])
                    person_id_list = [item['personId'] for item in person_ids]

                    api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/user_dashboard/user_dashboards_with_details/{user_id}'
                    response = requests.get(api_url, verify=server["server"]["verify"])
                    if response.status_code == 200:
                        dashboard_list = response.json().get('dashboards', [])
                        for dashboard in dashboard_list:
                            if dashboard['status'] is None:
                                dashboard['status'] = '정보없음'

                            if dashboard['personId'] in person_id_list:
                                dashboard_row.append(dashboard_item(
                                    dashboard['personId'],
                                    dashboard['name'],
                                    dashboard['gender'],
                                    dashboard['birth'],
                                    dashboard['status']
                                ))
                    else:
                        dashboard_row.append(no_row_item(initial=True))
                        return [html.Div(dashboard_row, style={'width': '100%', 'height': '100%',
                                                               'display': 'flex', 'align-itmes': 'center',
                                                               'justify-content': 'center'})]
                else:
                    dashboard_row.append(no_row_item(initial=True))
                    return [html.Div(dashboard_row, style={'width': '100%', 'height': '100%',
                                                           'display': 'flex', 'align-itmes': 'center',
                                                           'justify-content': 'center'})]
            except Exception as e:
                dashboard_row.append([])

            return [html.Div(dashboard_row)]

        elif pathname == '/beha-pulse/main/dashboard/delete/':
            dashboard_row = []
            user_id = session.get('user_id')
            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/user_dashboard_device/user_dashboard_devices/{user_id}/{session["selected_location"]}'
            try:
                response = requests.get(api_url, verify=server["server"]["verify"])
                if response.status_code == 200:
                    # 디바이스가 설치된 위치의 personId 목록을 가져옴 그걸 바탕으로 다시 personId에 해당하는 정보를 가져옴
                    person_ids = response.json().get('user_dashboard_device', [])
                    person_id_list = [item['personId'] for item in person_ids]

                    api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/user_dashboard/user_dashboards_with_details/{user_id}'
                    response = requests.get(api_url, verify=server["server"]["verify"])
                    if response.status_code == 200:
                        dashboard_list = response.json().get('dashboards', [])
                        for dashboard in dashboard_list:
                            if dashboard['status'] is None:
                                dashboard['status'] = '정보없음'

                            if dashboard['personId'] in person_id_list:
                                dashboard_row.append(dashboard_check_item(
                                    dashboard['personId'],
                                    dashboard['name'],
                                    dashboard['gender'],
                                    dashboard['birth'],
                                    dashboard['status']
                                ))
                    else:
                        dashboard_row.append(no_row_item(initial=False))
                        return [html.Div(dashboard_row, style={'width': '100%', 'height': '100%',
                                                               'display': 'flex', 'align-itmes': 'center',
                                                               'justify-content': 'center'})]
                else:
                    dashboard_row.append(no_row_item(initial=False))
                    return [html.Div(dashboard_row, style={'width': '100%', 'height': '100%',
                                                           'display': 'flex', 'align-itmes': 'center',
                                                           'justify-content': 'center'})]

            except Exception as e:
                dashboard_row.append([])

            return [html.Div(dashboard_row)]

    app.clientside_callback(
        """
        function(n_clicks, step, dashboard_data) {
            const MAX_STEP = 4;  // 최대 단계 설정
            
            if (!n_clicks || step >= MAX_STEP) {
                return [dashboard_data, step];  // n_clicks가 없거나 최대 단계에 도달하면 현재 단계 유지
            }

            // Step에 따라 입력 필드에서 값 가져오기
            let nameInput = document.getElementById('dashboard-add-input-name');
            
            let manButton = document.getElementById('dashboard-add-input-gender-man');
            let womanButton = document.getElementById('dashboard-add-input-gender-woman');
            
            let yearInput = document.getElementById('dashboard-add-input-year');
            let monthInput = document.getElementById('dashboard-add-input-month');
            let dayInput = document.getElementById('dashboard-add-input-day');
            
            if (!dashboard_data) {
                dashboard_data = {};
            }

            // 단계별로 데이터를 저장하고 검사 후 버튼 상태 변경
            if (step === 1 && nameInput) {
                dashboard_data['name'] = nameInput.value;                
                if (!dashboard_data['name']) {
                    alert('이름을 입력해주세요.');
                    return [dashboard_data, step];
                }
                console.log("Name stored: " + dashboard_data['name']);

            }
            else if (step === 2 && yearInput && monthInput && dayInput) {
                // 입력값을 숫자로 변환
                dashboard_data['year'] = parseInt(yearInput.value, 10);
                dashboard_data['month'] = parseInt(monthInput.value, 10);
                dashboard_data['day'] = parseInt(dayInput.value, 10);
                
                // 값이 비어 있으면 경고
                if (!dashboard_data['year'] || !dashboard_data['month'] || !dashboard_data['day']) {
                    alert('생년월일을 입력해주세요.');
                    return [dashboard_data, step];
                }
            
                // 생년월일 유효성 검사
                if (dashboard_data['year'] < 1900 || dashboard_data['year'] > new Date().getFullYear()) {
                    alert('올바른 연도를 입력해주세요.');
                    yearInput.value = '';
                    return [dashboard_data, step];
                }
                if (dashboard_data['month'] < 1 || dashboard_data['month'] > 12) {
                    alert('올바른 월을 입력해주세요.');
                    monthInput.value = '';
                    return [dashboard_data, step];
                }
            
                // 각 달의 최대 일수 확인 함수
                function getDaysInMonth(year, month) {
                    return new Date(year, month, 0).getDate();  // 해당 월의 마지막 날짜 반환
                }
            
                // 입력된 월의 최대 일수 확인
                let maxDays = getDaysInMonth(dashboard_data['year'], dashboard_data['month']);
                if (dashboard_data['day'] < 1 || dashboard_data['day'] > maxDays) {
                    alert(`올바른 일을 입력해주세요. ${dashboard_data['month']}월은 ${maxDays}일까지 있습니다.`);
                    dayInput.value = '';
                    return [dashboard_data, step];
                }
            
                // 생년월일 입력 양식 확인 yyyy mm dd (한 자리수 월/일의 경우 0 추가)
                dashboard_data['month'] = dashboard_data['month'] < 10 ? '0' + dashboard_data['month'] : dashboard_data['month'].toString();
                dashboard_data['day'] = dashboard_data['day'] < 10 ? '0' + dashboard_data['day'] : dashboard_data['day'].toString();
            
                console.log("Year stored: " + dashboard_data['year']);
                console.log("Month stored: " + dashboard_data['month']);
                console.log("Day stored: " + dashboard_data['day']);
            }
            
            else if (step === 3 && manButton && womanButton) {
                // 각 버튼의 상태를 직접 확인하여 성별 결정
                if (manButton.style.fontWeight === '900') {
                    dashboard_data['gender'] = 'male';
                } else if (womanButton.style.fontWeight === '900') {
                    dashboard_data['gender'] = 'female';
                }
                if (!dashboard_data['gender']) {
                    alert('성별을 선택해주세요.');
                    return [dashboard_data, step];
                }
                dashboard_data['FinalStep'] = true;
                console.log("Final Step stored: " + dashboard_data['FinalStep']);
                console.log("Gender stored: " + dashboard_data['gender']);
            }
            
            console.log("Updated dashboard_data :", dashboard_data);
            return [dashboard_data, step < MAX_STEP ? step + 1 : step];
        }
        """,
        [Output('dashboard-add-store', 'data'),
         Output('dashboard-add-current-step-store', 'data'), ],
        Input('dashboard-add-next-button', 'n_clicks'),
        [State('dashboard-add-current-step-store', 'data'),
         State('dashboard-add-store', 'data')],
    )

    @app.callback(
        [Output('dashboard-add-input-gender-man', 'style'),
         Output('dashboard-add-input-gender-woman', 'style')],
        [Input('dashboard-add-input-gender-man', 'n_clicks'),
         Input('dashboard-add-input-gender-woman', 'n_clicks')]
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
        if button_id == 'dashboard-add-input-gender-man':
            return active_style, default_style
        elif button_id == 'dashboard-add-input-gender-woman':
            return default_style, active_style
        else:
            return default_style, default_style

    @app.callback(
        [Output('dashboard-add-current-step-store', 'data', allow_duplicate=True),
         Output('dashboard-add', 'href')],
        [Input('dashboard-add-back-button', 'n_clicks')],
        [State('dashboard-add-current-step-store', 'data')],
        prevent_initial_call=True
    )
    def handle_back_button(n_clicks, current_step):
        if current_step == 1:
            return current_step, "/beha-pulse/main/dashboard/"  # 첫 페이지에서는 /beha-pulse/로 이동
        elif current_step == 5:
            return 1, "/beha-pulse/main/dashboard/"
        else:
            return current_step - 1, None  # 이전 단계로 이동

    # 현재 단계에 따라 signup-next-button의 텍스트를 동적으로 변경하는 콜백
    @app.callback(
        [Output('dashboard-add-next-button', 'children'),
         Output('dashboard-add-next-button', 'href')],
        [Input('dashboard-add-current-step-store', 'data')]
    )
    def update_next_button_text(current_step):
        if current_step == 4:
            return "홈화면으로 나가기", '/beha-pulse/main/dashboard/'
        else:
            return "다음", None

    @app.callback(
        [Output('dashboard-add-store', 'data', allow_duplicate=True),  # signup 데이터 업데이트
         Output('dashboard-add-current-step-store', 'data', allow_duplicate=True)],  # 단계 업데이트
        [Input('dashboard-add-next-button', 'n_clicks')],  # Next 버튼 클릭 감지
        [State('dashboard-add-store', 'data'),  # 현재 입력된 데이터
         State('dashboard-add-current-step-store', 'data')],  # 현재 단계
        prevent_initial_call=True
    )
    def register(n_clicks, data, step):
        if step == 3 and n_clicks and data['FinalStep']:
            required_fields = ['name', 'gender', 'year', 'month', 'day']
            if not all([data.get(key) for key in required_fields]):
                return data, 5  # 오류 단계로 설정

            birth = f"{data['year']}-{data['month']}-{data['day']}"
            gender = '남' if data['gender'] == 'male' else '여'

            payload = {
                'name': data['name'],
                'gender': gender,
                'birth': birth,
                'location': '',
            }
            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/dashboard/register'

            try:
                response = requests.post(api_url, json=payload, verify=server["server"]["verify"])
                if response.status_code == 200:
                    personId = response.json()['personId']
                    person_api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/user_dashboard/register'
                    person_payload = {
                        'personId': personId,
                        'userEmail': session.get('user_id')
                    }
                    person_response = requests.post(person_api_url, json=person_payload,
                                                    verify=server["server"]["verify"])
                    if person_response.status_code == 200:
                        return data, 4
                    else:
                        return data, 5
                else:
                    return data, 5
            except requests.exceptions.RequestException as e:
                return data, 5

        return no_update, no_update

    @app.callback(
        [Output('dashboard-delete-overlay-background', 'style', allow_duplicate=True),
         Output('delete-overlay-container', 'style', allow_duplicate=True),
         Output('delete-overlay-text', 'children', ),
         Output('delete-overlay-buttons', 'style')
         ],
        [Input('dashboard-delete-button-confirm', 'n_clicks'),
         Input('dashboard-delete-overlay-background', 'n_clicks'),
         Input({'type': 'checkbox', 'index': ALL}, 'value')
         ],
        [State('dashboard-delete-overlay-background', 'style'),
         State('delete-overlay-container', 'style')],
        prevent_initial_call=True
    )
    def toggle_overlay(n_clicks_button, n_clicks_background, selected_values, background_style, container_style):
        # 팝업을 켜는 경우
        ctx = callback_context
        if not ctx.triggered:
            return background_style, container_style
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        button_show = {'display': 'flex'}

        # 버튼 클릭으로 열기
        if triggered_id == 'dashboard-delete-button-confirm' and n_clicks_button:
            background_style['display'] = 'block'
            container_style['display'] = 'block'
        # 오버레이 클릭으로 닫기
        elif triggered_id == 'dashboard-delete-overlay-background' and n_clicks_background:
            background_style['display'] = 'none'
            container_style['display'] = 'none'

        # 선택된 personId 및 name 추출
        selected_persons = [value[0] for value in selected_values if value]  # 체크된 값에서 사전 데이터 추출

        # 선택된 이름 리스트
        selected_names = [person['name'] for person in selected_persons]

        # 선택된 사람 수에 따라 출력 텍스트 결정
        if len(selected_names) == 1:
            # text = f"{selected_names[0]} 님을 <br> 정말 삭제하시겠습니까?"
            text = [f"{selected_names[0]} 님을", html.Br(), "정말 삭제하시겠습니까?"]
        elif len(selected_names) > 1:
            text = [f"{selected_names[0]} 외 {len(selected_names) - 1}명을", html.Br(), "삭제하시겠습니까?"]
        else:
            text = "아무도 선택 되지 않았습니다."  # 선택된 사람이 없는 경우
            button_show = {'display': 'none'}

        return background_style, container_style, text, button_show

    @app.callback(
        Output('dashboard-delete', 'href'),
        Input('delete-confirm-button', 'n_clicks'),
        [State({'type': 'checkbox', 'index': ALL}, 'value')],
    )
    def delete_dashboard(n_clicks, selected_values):
        if n_clicks:
            selected_persons = [value[0] for value in selected_values if value]  # 체크된 값에서 사전 데이터 추출

            selected_names = [person['name'] for person in selected_persons]
            selected_ids = [person['personId'] for person in selected_persons]

            del_count = 0
            for idx in range(len(selected_persons)):

                api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/dashboard/delete/{selected_ids[idx]}/{selected_names[idx]}'

                try:
                    response = requests.delete(api_url, verify=server["server"]["verify"])
                    if response.status_code == 200:
                        del_count += 1
                    else:
                        return no_update

                except requests.exceptions.RequestException as e:
                    return no_update
            if del_count == len(selected_persons):
                return '/beha-pulse/main/dashboard/'
            else:
                return no_update
        return no_update

    @app.callback(
        [Output('dashboard-delete-overlay-background', 'style', allow_duplicate=True),
         Output('delete-overlay-container', 'style', allow_duplicate=True),
         Input('delete-cancel-button', 'n_clicks')],
        [State('dashboard-delete-overlay-background', 'style'),
         State('delete-overlay-container', 'style')],
        prevent_initial_call=True
    )
    def cancel_delete(n_clicks, background_style, container_style):
        if n_clicks:
            background_style['display'] = 'none'
            container_style['display'] = 'none'
        return background_style, container_style

    @app.callback(
        Output('redirect', 'href', allow_duplicate=True),
        Input('not-connected-back-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def not_connected_back(n_clicks):
        if n_clicks:
            return '/beha-pulse/main/dashboard/'
        return no_update

    @app.callback(
        Output('dashboard-not-connected-rows', 'children'),
        Input('url', 'pathname'),
    )
    def not_connected_rows(pathname):
        if pathname == '/beha-pulse/main/dashboard/not-connected/':
            dashboard_row = []

            user_id = session.get('user_id')
            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/user_dashboard_device/user_dashboard_devices/{user_id}'
            try:
                response = requests.get(api_url, verify=server["server"]["verify"])
                if response.status_code == 200:
                    user_dashboard_device = response.json().get('user_dashboard_device', [])
                    connected_person_ids = [item['personId'] for item in user_dashboard_device]
                    print(connected_person_ids)
                    api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/user_dashboard/user_dashboards/{user_id}'
                    response = requests.get(api_url, verify=server["server"]["verify"])
                    if response.status_code == 200:
                        dashboard_list = response.json().get('dashboards', [])
                        person_ids = [dashboard[1] for dashboard in dashboard_list]
                        not_connected_person_ids = list(set(person_ids) - set(connected_person_ids))
                        # 아이디를 가지고 다시 정보를 가져옴
                        for person_id in not_connected_person_ids:
                            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/dashboard/{person_id}'
                            response = requests.get(api_url, verify=server["server"]["verify"])
                            if response.status_code == 200:
                                dashboard = response.json().get('dashboard', {})
                                if dashboard['status'] is None:
                                    dashboard['status'] = '정보없음'
                                dashboard_row.append(dashboard_not_connected_item(
                                    dashboard['personId'],
                                    dashboard['name'],
                                    dashboard['gender'],
                                    dashboard['birth'],
                                    dashboard['status']
                                ))
                    else:
                        dashboard_row.append(no_row_item(initial=True))
                        return [html.Div(dashboard_row, style={'width': '100%', 'height': '100%',
                                                               'display': 'flex', 'align-itmes': 'center',
                                                               'justify-content': 'center'})]
                else:
                    dashboard_row.append(no_row_item(initial=True))
                    return [html.Div(dashboard_row, style={'width': '100%', 'height': '100%',
                                                           'display': 'flex', 'align-itmes': 'center',
                                                           'justify-content': 'center'})]

            except Exception as e:
                dashboard_row.append([])

            return [html.Div(dashboard_row)]

    @app.callback(
        Output('redirect', 'href', allow_duplicate=True),
        Input('dashboard-detail-back-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def not_connected_back(n_clicks):
        if n_clicks:
            return '/beha-pulse/main/dashboard/'
        return no_update

    @app.callback(
        Output('dashboard', 'href'),
        Input({'type': 'dashboard-row', 'index': ALL}, 'n_clicks'),
    )
    def control_row_click(n_clicks):
        ctx = callback_context

        # index 중에서 클릭이 발생했을 때에만
        if not ctx.triggered or not n_clicks or all(click is None or click == 0 for click in n_clicks):
            raise PreventUpdate

        clicked_id = None
        for i, click in enumerate(n_clicks):
            if click and i < len(ctx.inputs_list[0]):  # 인덱스 범위 내에서 참조
                clicked_id = ctx.inputs_list[0][i]['id']['index']
                break

        if not clicked_id:
            raise PreventUpdate

        if clicked_id:
            session['detail_person_id'] = clicked_id

            # 그려야할 디바이스 맥주소 확인
            user_id = session.get('user_id')
            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/user_dashboard_device/user_dashboard_devices/device/{user_id}/{clicked_id}'
            response = requests.get(api_url, verify=server["server"]["verify"])
            mac_address_list = []
            device_list = []
            if response.status_code == 200:
                user_dashboard_device = response.json().get('user_dashboard_device', [])
                device_list = [item[3] for item in user_dashboard_device]

                # API 호출로 맥주소 가져옴
                for device in device_list:
                    api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/device/{device}'
                    response = requests.get(api_url, verify=server["server"]["verify"])
                    if response.status_code == 200:
                        device_info = response.json().get('device', {})
                        mac_address_list.append(device_info['macAddress'])
                        session['mac_address_list'] = mac_address_list

            return '/beha-pulse/main/dashboard/detail/'

        else:
            raise PreventUpdate

    @app.callback(
        Output('dashboard-profile-image', 'src'),
        Input('url', 'pathname'),
    )
    def set_profile_image(pathname):
        if pathname == '/beha-pulse/main/dashboard/detail/':
            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/dashboard/{session["detail_person_id"]}'
            try:
                response = requests.get(api_url, verify=server["server"]["verify"])
                if response.status_code == 200:
                    user = response.json().get('dashboard')
                    if user['gender'] == '남':
                        return '../../../assets/img/man_profile.svg'
                    else:
                        return '../../../assets/img/girl_profile.svg'

                else:
                    return no_update
            except requests.exceptions.RequestException as e:
                return no_update
        return no_update

    # 슬라이드 이동을 제어하는 콜백
    @app.callback(
        Output('dashboard-slider-container', 'style'),
        [Input('dashboard-slider-forward-button-1', 'n_clicks'),
         Input('dashboard-slider-back-button-1', 'n_clicks'),
         Input('dashboard-slider-forward-button-2', 'n_clicks'),
         Input('dashboard-slider-back-button-2', 'n_clicks'),
         Input('dashboard-slider-forward-button-3', 'n_clicks'),
         Input('dashboard-slider-back-button-3', 'n_clicks'),
         ],
        State('dashboard-slider-container', 'style')
    )
    def slide(n_clicks_forward_1, n_clicks_back_1, n_clicks_forward_2, n_clicks_back_2, n_clicks_forward_3,
              n_clicks_back_3, style):
        # 어떤 버튼을 클릭했는지 확인
        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        n_clicks = 0

        if button_id == 'dashboard-slider-forward-button-1':
            n_clicks = 1
        elif button_id == 'dashboard-slider-back-button-1':
            n_clicks = 2
        elif button_id == 'dashboard-slider-forward-button-2':
            n_clicks = 2
        elif button_id == 'dashboard-slider-back-button-2':
            n_clicks = 0
        elif button_id == 'dashboard-slider-forward-button-3':
            n_clicks = 0
        elif button_id == 'dashboard-slider-back-button-3':
            n_clicks = 1

        # 슬라이드 인덱스 계산
        index = n_clicks % 3
        # 슬라이드의 가로 이동 비율 계산 (각 슬라이드는 100%씩 이동)
        translate_value = -(index * 100) / 3
        # 슬라이드 컨테이너의 transform 속성 업데이트
        style['transform'] = f'translateX({translate_value}%)'
        return style

    @app.callback(
        [Output('dashboard-profile-name', 'children'),
         Output('dashboard-profile-gender', 'children'),
         Output('dashboard-profile-birth', 'children'),
         Output('dashboard-profile-age', 'children'), ],
        Input('url', 'pathname'),
    )
    def set_profile(pathname):
        if pathname == '/beha-pulse/main/dashboard/detail/':
            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/dashboard/{session["detail_person_id"]}'
            try:
                response = requests.get(api_url, verify=server["server"]["verify"])
                if response.status_code == 200:
                    user = response.json().get('dashboard')
                    name = user['name']
                    gender = user['gender']
                    birth = user['birth']
                    # 생일이 지났는지 판단
                    today = datetime.now()
                    birth_date = datetime.strptime(birth, '%Y-%m-%d')
                    formatted_birth_date = birth_date.strftime('%Y%m%d')
                    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                    return [name, gender, formatted_birth_date, f"만 {age}세"]
                else:
                    return ["정보 없음", "정보 없음", "정보 없음", "정보 없음"]
            except requests.exceptions.RequestException as e:
                return ["정보 없음", "정보 없음", "정보 없음", "정보 없음"]

        return ["정보 없음", "정보 없음", "정보 없음", "정보 없음"]

    @app.callback(
        [Output('dashboard-profile-status-lying-text', 'children'),
         Output('dashboard-profile-status-lying-time', 'children'),
         Output('dashboard-profile-status-empty-text', 'children'),
         Output('dashboard-profile-status-empty-time', 'children'),
         Output('dashboard-profile-status-sitting-text', 'children'),
         Output('dashboard-profile-status-sitting-time', 'children')],
        Input('url', 'pathname'),
    )
    def set_profile_status(pathname):
        if pathname == '/beha-pulse/main/dashboard/detail/':
            lying_txt = ""
            empty_txt = ""
            sitting_txt = ""
            lying_time = ""
            empty_time = ""
            sitting_time = ""

            date = datetime.now().strftime('%Y-%m-%d')
            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/state_inference/list/{session["detail_person_id"]}/{date}'
            try:
                response = requests.get(api_url, verify=server["server"]["verify"])
                if response.status_code == 200:
                    log_list = response.json().get('state_inference')
                    if log_list:
                        # 로그를 'inferenceTime' 기준으로 정렬
                        log_list.sort(key=lambda x: x['inferenceTime'])

                        # 마지막 상태를 찾고, 그 상태가 언제부터 지속되었는지 계산
                        last_log_status = log_list[-1]['inferencedStatus']
                        last_change_time = None

                        # 상태가 바뀌는 시점을 찾음
                        for i in range(len(log_list) - 1, -1, -1):
                            if log_list[i]['inferencedStatus'] != last_log_status:
                                last_change_time = datetime.strptime(log_list[i + 1]['inferenceTime'],
                                                                     '%Y-%m-%d %H:%M:%S')
                                break
                        else:
                            # 만약 상태 변화가 없으면 첫 번째 로그부터 지속된 것으로 간주
                            last_change_time = datetime.strptime(log_list[0]['inferenceTime'], '%Y-%m-%d %H:%M:%S')

                        # 현재까지의 지속 시간 계산
                        continue_time = datetime.now() - last_change_time
                        continue_time = continue_time.total_seconds() // 60
                        continue_time_text = f"{int(continue_time // 60)}시간 {int(continue_time % 60)}분"

                        # 현재 상태에 따라 텍스트와 시간을 설정
                        if last_log_status == '누워있음':
                            lying_txt = "현재 지속시간"
                            lying_time = continue_time_text

                            empty_txt = "마지막 활동"
                            empty_time = next(
                                (datetime.strptime(log['inferenceTime'], '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S')
                                 for log in reversed(log_list) if log['inferencedStatus'] == '비어있음'), "없음")

                            sitting_txt = "마지막 활동"
                            sitting_time = next(
                                (datetime.strptime(log['inferenceTime'], '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S')
                                 for log in reversed(log_list) if log['inferencedStatus'] == '앉아있음'), "없음")

                        elif last_log_status == '비어있음':
                            empty_txt = "현재 지속시간"
                            empty_time = continue_time_text

                            lying_txt = "마지막 활동"
                            lying_time = next(
                                (datetime.strptime(log['inferenceTime'], '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S')
                                 for log in reversed(log_list) if log['inferencedStatus'] == '누워있음'), "없음")

                            sitting_txt = "마지막 활동"
                            sitting_time = next(
                                (datetime.strptime(log['inferenceTime'], '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S')
                                 for log in reversed(log_list) if log['inferencedStatus'] == '앉아있음'), "없음")

                        elif last_log_status == '앉아있음':
                            sitting_txt = "현재 지속시간"
                            sitting_time = continue_time_text

                            lying_txt = "마지막 활동"
                            lying_time = next(
                                (datetime.strptime(log['inferenceTime'], '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S')
                                 for log in reversed(log_list) if log['inferencedStatus'] == '누워있음'), "없음")

                            empty_txt = "마지막 활동"
                            empty_time = next(
                                (datetime.strptime(log['inferenceTime'], '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S')
                                 for log in reversed(log_list) if log['inferencedStatus'] == '비어있음'), "없음")

                        else:
                            return ["마지막 활동", "없음", "마지막 활동", "없음", "마지막 활동", "없음"]

                        # 세션에 값 저장
                        session['lying_txt'] = lying_txt
                        session['lying_time'] = lying_time
                        session['empty_txt'] = empty_txt
                        session['empty_time'] = empty_time
                        session['sitting_txt'] = sitting_txt
                        session['sitting_time'] = sitting_time

                        return [lying_txt, lying_time, empty_txt, empty_time, sitting_txt, sitting_time]

                    # 로그가 비어있을 때
                    return ["마지막 활동", "없음", "마지막 활동", "없음", "마지막 활동", "없음"]

                else:
                    # 응답 코드가 200이 아닐 때
                    return ["마지막 활동", "없음", "마지막 활동", "없음", "마지막 활동", "없음"]

            except requests.exceptions.RequestException as e:
                # 요청 예외가 발생할 때
                return ["마지막 활동", "없음", "마지막 활동", "없음", "마지막 활동", "없음"]

        # 경로가 일치하지 않을 때
        return ["", "", "", "", "", ""]

    import time

    @app.callback(
        Output('live-graph', 'figure'),
        [Input('graph-update', 'n_intervals'),
         Input('url', 'pathname')],
        prevent_initial_call=True
    )
    def update_graph(n_intervals, pathname):
        if n_intervals is None or n_intervals == 0:
            raise PreventUpdate

        if pathname == '/beha-pulse/main/dashboard/detail/':
            # 세션에서 시각화할 MAC 주소 목록을 가져옴
            # 해당 사용자에게 매칭된 디바이스의 맥 주소를 모두 가져옴
            mac_address_list = session.get('mac_address_list')
            if mac_address_list:
                traces = []

                for mac_address in mac_address_list:
                    # Flask API를 호출하여 특정 MAC 주소의 최신 CSI 데이터를 가져옴
                    api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/device/CSI/{mac_address}'
                    response = requests.get(api_url, verify=server["server"]["verify"])

                    if response.status_code == 200:
                        amp_data = response.json()
                        # amp_data = amp_data[0:100]  # 최근 100개의 데이터 포인트만 사용
                        if amp_data:
                            # X축 데이터 생성 (가장 최근 100개의 데이터 포인트)
                            x_data = list(range(len(amp_data)))

                            # Y축 데이터는 44번째 서브캐리어의 암시적 진폭 (예시)
                            y_data = [amplitude[44] for amplitude in amp_data if len(amplitude) > 44]

                            trace = go.Scatter(
                                x=x_data,
                                y=y_data,
                                mode='lines',
                                name=f'MAC {mac_address}',  # MAC 주소별로 이름을 부여
                                line={'width': 2}
                            )
                            traces.append(trace)

                figure = {
                    'data': traces,
                    'layout': go.Layout(
                        # title='Amplitude of Subcarrier 44 for Multiple MAC Addresses',
                        xaxis={'title': 'Time', 'range': [0, 100]},
                        yaxis={'title': 'Amplitude', 'range': [0, 40]},
                        autosize=True,
                        margin=dict(l=0, r=0, t=0, b=0),
                        paper_bgcolor='white',
                        plot_bgcolor='white',
                        showlegend=False
                    )
                }

                return figure

            return {}
        else:
            raise PreventUpdate

    # @app.callback(
    #     Output('live-graph', 'figure'),
    #     [Input('graph-update', 'n_intervals')]
    # )
    # def update_graph_live(n):
    #     # 예시 데이터 생성
    #     x_data = list(range(100))
    #     import random
    #     y_data = [random.randint(0, 40) for _ in range(100)]
    #
    #     figure = go.Figure(
    #         data=[go.Scatter(
    #             x=x_data,
    #             y=y_data,
    #             mode='lines',
    #             line={'width': 2}
    #
    #         )],
    #         layout=go.Layout(
    #             xaxis={'title': 'Time', 'range': [0, 100]},
    #             yaxis={'title': 'Amplitude', 'range': [0, 40]},
    #             autosize=True,
    #             margin=dict(l=0, r=0, t=0, b=0),
    #             paper_bgcolor='white',
    #             plot_bgcolor='white',
    #         )
    #     )
    #
    #     return figure
