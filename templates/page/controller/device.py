from dash.exceptions import PreventUpdate

from app import admin_app
from flask import Flask, session
from dash import Dash, dcc, html, callback_context, no_update
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
import requests
import json
from datetime import datetime

from ..layout.content.device.device_detail import *
from ..layout.content.device.device_edit import *
from ..layout.content.device.device import device_item

with open('config/server.json', 'r') as f:
    server = json.load(f)


def user_overlay_item(label, personId):
    return html.Div(label, style={'font-size': '18px', 'padding': '10px', 'cursor': 'pointer'},
                    id={'type': 'user_overlay_location', 'index': label, 'personId': personId},  # 각 줄에 고유 id 부여
                    )


def no_row_item(initial=True):
    if initial:
        src = '../../assets/img/error.svg'
    else:
        src = '../../../assets/img/error.svg'
    return html.Div([
        html.Img(src=src, style={'width': '15vh', 'height': '15vh'}),
        html.Span("등록된 장치가 없습니다.", style={'font-weight': 'bold', 'font-size': '20px', 'margin-top': '20px'}),
    ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'height': '100%',
              'flex-direction': 'column'})


def convert_bool_to_on_off(value):
    if value:
        return 'active'
    return 'inactive'


def device_controller(app):
    @app.callback(
        [Output('device-rows', 'children')],
        Input('url', 'pathname'),
    )
    def set_device_list_row(pathname):
        if pathname == '/beha-pulse/main/device/':
            user_id = session.get('user_id')  # 세션에서 user_id를 가져옴

            # 장치 정보를 저장할 리스트 초기화
            device_rows = []

            # 유저 장치 목록과 세부 정보를 한 번에 가져오는 API 호출
            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/user_device/user_devices_with_details/{user_id}'

            try:
                # API 호출
                response = requests.get(api_url, verify=server["server"]["verify"])
                if response.status_code == 200:
                    device_list = response.json().get('user_devices', [])

                    # 각 장치 정보를 기반으로 UI 구성
                    for device in device_list:
                        if device['location'] == "":
                            device['location'] = "장소 미설정"
                        if device['location'] == session['selected_location']:
                            device_rows.append(device_item(
                                device.get('type', 'Unknown'),
                                device.get('macAddress', 'Unknown'),
                                convert_bool_to_on_off(device.get('on_off', 'inactive'))
                            ))

                else:
                    # API 호출 실패 시 에러 메시지 추가
                    device_rows.append(no_row_item(initial=True))
                    return [html.Div(device_rows, style={'width': '100%', 'height': '100%',
                                                         'display': 'flex', 'align-itmes': 'center',
                                                         'justify-content': 'center'})]

            except requests.exceptions.RequestException as e:
                # API 호출 중 예외 발생 시 처리
                device_rows.append(html.Div("RequestException occurred"))

            # 성공적으로 데이터를 처리한 경우 반환
            # return [html.Div(device_rows, style={'width': '100%', 'height': '100%',
            #                                    'display': 'flex', 'align-itmes': 'center',
            #                                    'justify-content': 'center'})]
            return [html.Div(device_rows)]

        # URL이 '/beha-pulse/main/device/'가 아닌 경우 업데이트하지 않음
        return no_update

    @app.callback(
        Output('device', 'href'),  # 출력은 화면에 표시되지 않음
        Input({'type': 'device-row', 'index': ALL}, 'n_clicks'),
        prevent_initial_call=True
    )
    def device_row_click(n_clicks):
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
            session['selected_device_mac_address'] = clicked_id
            return '/beha-pulse/main/device/detail/'
        else:
            raise PreventUpdate

    @app.callback(
        Output('device-detail', 'href', allow_duplicate=True),
        Input('device-detail-back-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def back_to_device_list(n_clicks):
        if n_clicks:
            return "/beha-pulse/main/device/"

    @app.callback(
        Output('device-detail-main-content', 'children'),
        Input('url', 'pathname'),
    )
    def set_device_detail(pathname):
        if pathname == '/beha-pulse/main/device/detail/':
            mac_address = session['selected_device_mac_address']
            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/device/{mac_address}'
            try:
                response = requests.get(api_url, verify=server["server"]["verify"])
                if response.status_code == 200:
                    device = response.json().get('device', {})
                    device_id = device.get('deviceId')
                    # 상태를 ON/OFF에 따라 색상 변경 적용
                    on_off_status = 'ON' if device.get('on_off') else 'OFF'

                    find_person_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/user_dashboard_device/user_dashboard_devices/person/{session["user_id"]}/{device_id}'
                    person_response = requests.get(find_person_url, verify=server["server"]["verify"])
                    if person_response.status_code == 200:
                        person_data = person_response.json().get('user_dashboard_device', {})
                        person_id = person_data[2]
                        find_name_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/dashboard/{person_id}'
                        name_response = requests.get(find_name_url, verify=server["server"]["verify"])
                        if name_response.status_code == 200:
                            device['person_name'] = name_response.json().get('dashboard').get('name')

                    return [
                        info_row('ic-manufacturing', '장치', device.get('type', 'N/A')),
                        info_row('ic-computer', 'MAC 주소', device.get('macAddress', 'N/A')),
                        info_row('ic-local-hospital', '설치 장소', device.get('install_location', 'N/A')),
                        info_row('ic-location-on', '설치 위치', device.get('room', 'N/A')),
                        info_row('ic-calendar-month', '점검 날짜', device.get('check_date', 'N/A')),
                        info_row('ic-offline-bolt', '상태', on_off_status, status=on_off_status),
                        info_row('ic-display-settings', '노트', device.get('note', 'N/A')),
                        info_row('ic-person-device', '사용자', device.get('person_name', '미등록'))
                    ]
                else:
                    return html.Div([])
            except requests.exceptions.RequestException as e:
                # 요청 예외 발생 시 처리
                return html.Div(f"RequestException occurred: {e}")
        else:
            return no_update

    @app.callback(
        Output('device-edit', 'href'),
        Input('device-edit-back-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def back_to_device_list(n_clicks):
        if n_clicks:
            return "/beha-pulse/main/device/detail/"

    @app.callback(
        [Output('on-button', 'style'),
         Output('off-button', 'style')],
        [Input('on-button', 'n_clicks'),
         Input('off-button', 'n_clicks')],
        [State('on-button', 'style'), State('off-button', 'style')],
        prevent_initial_call=True
    )
    def on_off_style_change(on_clicks, off_clicks, on_style, off_style):
        ctx = callback_context
        if not ctx.triggered:
            return on_style, off_style

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'on-button':
            on_style['color'] = '#00D84F'
            off_style['color'] = 'black'
            on_style['font-weight'] = 'bold'
            off_style['font-weight'] = 'normal'
        elif button_id == 'off-button':
            on_style['color'] = 'black'
            off_style['color'] = '#E10000'
            on_style['font-weight'] = 'normal'
            off_style['font-weight'] = 'bold'

        return on_style, off_style

    @app.callback(
        Output('device-edit-main-content', 'children'),
        Input('url', 'pathname'),
    )
    def set_device_edit_value(pathname):
        if pathname == '/beha-pulse/main/device/edit/':
            mac_address = session['selected_device_mac_address']
            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/device/{mac_address}'
            try:
                response = requests.get(api_url, verify=server["server"]["verify"])
                if response.status_code == 200:
                    device = response.json().get('device', {})
                    device_id = device.get('deviceId')
                    on_off_status = 'ON' if device.get('on_off') else 'OFF'

                    if on_off_status == 'ON':
                        on_status_color = '#00D84F',
                        off_status_color = 'black'
                        on_status_weight = 'bold'
                        off_status_weight = 'normal'
                    else:
                        on_status_color = 'black'
                        off_status_color = '#E10000'
                        on_status_weight = 'normal'
                        off_status_weight = 'bold'

                    on_style = {
                        'cursor': 'pointer',
                        'color': on_status_color,
                        'font-size': '1rem',
                        'align-items': 'center',
                        'font-weight': on_status_weight
                    }
                    off_style = {
                        'cursor': 'pointer',
                        'color': off_status_color,
                        'font-size': '1rem',
                        'align-items': 'center',
                        'font-weight': off_status_weight
                    }

                    find_person_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/user_dashboard_device/user_dashboard_devices/person/{session["user_id"]}/{device_id}'
                    person_response = requests.get(find_person_url, verify=server["server"]["verify"])
                    if person_response.status_code == 200:
                        person_data = person_response.json().get('user_dashboard_device', {})
                        person_id = person_data[2]
                        find_name_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/dashboard/{person_id}'
                        name_response = requests.get(find_name_url, verify=server["server"]["verify"])
                        if name_response.status_code == 200:
                            device['person_name'] = name_response.json().get('dashboard').get('name')
                    return [
                        edit_row('ic-manufacturing', '장치', device.get('type', 'N/A'), '장치'),
                        edit_row('ic-computer', 'MAC 주소', device.get('macAddress', 'N/A'), 'MAC 주소'),
                        edit_row('ic-local-hospital', '설치 장소', device.get('install_location', 'N/A'), '설치 장소'),
                        edit_row('ic-location-on', '설치 위치', device.get('room', 'N/A'), '설치 위치'),
                        edit_row('ic-calendar-month', '점검 날짜', device.get('check_date', 'N/A'), 'YYYY-MM-DD'),
                        edit_on_off('ic-offline-bolt', on_style, off_style),
                        edit_row('ic-display-settings', '노트', device.get('note', 'N/A'), '메모'),
                        edit_click('ic-person-device', '사용자', device.get('person_name', '미등록'), '사용자')
                    ]
                else:
                    return html.Div(f"Error fetching device details: {response.status_code}")
            except requests.exceptions.RequestException as e:
                # 요청 예외 발생 시 처리
                return html.Div(f"RequestException occurred: {e}")
        else:
            return no_update

    @app.callback(
        Output('device-edit', 'href', allow_duplicate=True),
        Input('device-edit-save-button', 'n_clicks'),
        [State('device-edit-input-장치', 'value'),
         State('device-edit-input-MAC 주소', 'value'),
         State('device-edit-input-설치 장소', 'value'),
         State('device-edit-input-설치 위치', 'value'),
         State('device-edit-input-점검 날짜', 'value'),
         State('on-button', 'style'),
         State('off-button', 'style'),
         State('device-edit-input-노트', 'value'),
         State('device-edit-store', 'data'),
         ],
        prevent_initial_call=True
    )
    def save_device_edit(n_clicks, device_type, mac_address, install_location, room, check_date, on_style, off_style,
                         note, data):
        person_id = data.get('personId')
        if n_clicks:
            if not all([device_type]):
                return html.Div("Please fill out all required fields.")

            if on_style['color'] == '#00D84F':
                on_off = "1"
            else:
                on_off = "0"

            try:
                check_date = datetime.strptime(check_date, "%Y-%m-%d").date()
                check_date_str = check_date.isoformat()  # Convert to string in ISO format (YYYY-MM-DD)

            except ValueError:
                raise no_update

            data = {
                'type': device_type,
                'macAddress': mac_address,
                'install_location': install_location,
                'room': room,
                'check_date': check_date_str,
                'on_off': on_off,
                'note': note,
            }

            mac_address = session['selected_device_mac_address']
            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/device/update/{mac_address}'
            try:
                response = requests.put(api_url, json=data, verify=server["server"]["verify"])
                if response.status_code == 200:
                    response_data = response.json().get('device')
                    device_id = response_data.get('deviceId')
                    user_email = session.get('user_id')
                    user_device_api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/user_dashboard_device/update/{user_email}/{device_id}'
                    user_device_data = {
                        "userEmail": user_email,
                        "deviceId": device_id,
                        "personId": person_id
                    }
                    user_device_response = requests.put(user_device_api_url, json=user_device_data, verify=server["server"]["verify"])
                    if user_device_response.status_code == 200:
                        return "/beha-pulse/main/device/detail/"

                    elif user_device_response.status_code == 404:
                        api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/user_dashboard_device/register'
                        user_device_data = {
                            "userEmail": user_email,
                            "deviceId": device_id,
                            "personId": person_id
                        }
                        user_device_response = requests.post(api_url, json=user_device_data, verify=server["server"]["verify"])
                        if user_device_response.status_code == 200:
                            return "/beha-pulse/main/device/detail/"

                else:
                    return no_update
            except requests.exceptions.RequestException as e:
                # 요청 예외 발생 시 처리
                return no_update
        else:
            return no_update

    @app.callback(
        Output('device-add', 'href'),
        Input('device-add-back-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def back_to_device_list(n_clicks):
        if n_clicks:
            return "/beha-pulse/main/device/"

    @app.callback(
        Output('device-add', 'href', allow_duplicate=True),
        Input('device-add-save-button', 'n_clicks'),
        [State('device-add-input-장치', 'value'),
         State('device-add-input-MAC 주소', 'value'),
         State('device-add-input-설치 장소', 'value'),
         State('device-add-input-설치 위치', 'value'),
         State('device-add-input-점검 날짜', 'value'),
         State('on-button', 'style'),
         State('off-button', 'style'),
         State('device-add-input-노트', 'value')],
        prevent_initial_call=True
    )
    def save_device_add(n_clicks, device_type, mac_address, install_location, room, check_date, on_style, off_style,
                        note):
        if n_clicks:
            if not all([device_type]):
                return html.Div("Please fill out all required fields.")

            if on_style['color'] == '#00D84F':
                on_off = "1"
            else:
                on_off = "0"

            try:
                check_date = datetime.strptime(check_date, "%Y-%m-%d").date()
                check_date_str = check_date.isoformat()  # Convert to string in ISO format (YYYY-MM-DD)

            except ValueError:
                raise no_update

            data = {
                'type': device_type,
                'macAddress': mac_address,
                'install_location': install_location,
                'room': room,
                'check_date': check_date_str,
                'on_off': on_off,
                'note': note
            }

            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/device/register'
            try:
                response = requests.post(api_url, json=data, verify=server["server"]["verify"])
                print(response.json())
                if response.status_code == 200:
                    user_device_api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/user_device/register'
                    user_device_data = {
                        'userEmail': session.get('user_id'),
                        'macAddress': mac_address
                    }
                    user_device_response = requests.post(user_device_api_url, json=user_device_data, verify=server["server"]["verify"])
                    if user_device_response.status_code == 200:
                        return "/beha-pulse/main/device/"
                    else:
                        return no_update
                else:
                    return no_update
            except requests.exceptions.RequestException as e:
                # 요청 예외 발생 시 처리
                return no_update
        else:
            return no_update

    @app.callback(
        [Output('device-overlay-background', 'style', allow_duplicate=True),
         Output('device-delete-overlay-container', 'style', allow_duplicate=True),
         Output('device-delete-overlay-text', 'children', ),
         ],
        [Input('device-delete-button', 'n_clicks'),
         Input('device-overlay-background', 'n_clicks'),
         ],
        [State('device-overlay-background', 'style'),
         State('device-delete-overlay-container', 'style')]
        , prevent_initial_call=True
    )
    def delete_overlay(n_clicks, background_clicks, background_style, overlay_style):
        ctx = callback_context
        if not ctx.triggered:
            return background_style, overlay_style
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == 'device-delete-button' and n_clicks:
            background_style['display'] = 'block'
            overlay_style['display'] = 'block'
            return background_style, overlay_style, '장치를 삭제하시겠습니까?',
        elif triggered_id == 'device-overlay-background' and background_clicks:
            background_style['display'] = 'none'
            overlay_style['display'] = 'none'
            return background_style, overlay_style, '',
        else:
            return no_update

    @app.callback(
        [Output('device-overlay-background', 'style', allow_duplicate=True),
         Output('device-delete-overlay-container', 'style', allow_duplicate=True),
         Input('device-delete-cancel-button', 'n_clicks')],
        [State('device-overlay-background', 'style'),
         State('device-delete-overlay-container', 'style')],
        prevent_initial_call=True
    )
    def cancel_delete(n_clicks, background_style, container_style):
        if n_clicks:
            background_style['display'] = 'none'
            container_style['display'] = 'none'
        return background_style, container_style

    @app.callback(
        [Output('device-user-overlay-background', 'style', allow_duplicate=True),
         Output('device-user-overlay-container', 'style', allow_duplicate=True),
         ],
        [Input('device-edit-input-사용자', 'n_clicks'),
         Input('device-user-overlay-background', 'n_clicks'),
         ],
        [State('device-user-overlay-background', 'style'),
         State('device-user-overlay-container', 'style')]
        , prevent_initial_call=True
    )
    def user_select_overlay(n_clicks, background_clicks, background_style, overlay_style):
        ctx = callback_context
        if not ctx.triggered:
            return background_style, overlay_style
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if triggered_id == 'device-edit-input-사용자' and n_clicks:
            background_style['display'] = 'block'
            overlay_style['display'] = 'block'
            return background_style, overlay_style
        elif triggered_id == 'device-user-overlay-background' and background_clicks:
            background_style['display'] = 'none'
            overlay_style['display'] = 'none'
            return background_style, overlay_style
        else:
            return no_update

    @app.callback(
        Output('device-user-overlay-content', 'children'),
        Input('device-edit-input-사용자', 'n_clicks'),
    )
    def set_overlay_user_list(n_clicks):
        if n_clicks:
            user_id = session.get('user_id')
            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/user_dashboard/user_dashboards_with_details/{user_id}'
            try:
                response = requests.get(api_url, verify=server["server"]["verify"])
                if response.status_code == 200:
                    user_list = response.json().get('dashboards', [])
                    user_name_overlay_list = []
                    for user in user_list:
                        user_name_overlay_list.append(user_overlay_item(user.get('name'), user.get('personId')))

                    return user_name_overlay_list

            except requests.exceptions.RequestException as e:
                return html.Div(f"RequestException occurred: {e}")
        else:
            return no_update

    @app.callback(
        [Output('device-edit-input-사용자', 'children'),
         Output('device-edit-store', 'data'),
         Output('device-user-overlay-background', 'style', allow_duplicate=True),
         Output('device-user-overlay-container', 'style', allow_duplicate=True), ],
        Input({'type': 'user_overlay_location', 'index': ALL, 'personId': ALL}, 'n_clicks'),
        [State('device-user-overlay-background', 'style'),
         State('device-user-overlay-container', 'style')
         ],
        prevent_initial_call=True
    )
    def select_user(n_clicks, background_style, overlay_style):
        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate

        clicked_id = None
        clicked_person_id = None
        for i, click in enumerate(n_clicks):
            if click and i < len(ctx.inputs_list[0]):  # 인덱스 범위 내에서 참조
                clicked_id = ctx.inputs_list[0][i]['id']['index']
                clicked_person_id = ctx.inputs_list[0][i]['id']['personId']
                break

        if not clicked_id:
            raise PreventUpdate

        print(clicked_id)
        print(clicked_person_id)

        user_data = {
            'name': clicked_id,
            'personId': clicked_person_id
        }

        if clicked_id:
            background_style['display'] = 'none'
            overlay_style['display'] = 'none'
        return clicked_id, user_data, background_style, overlay_style

    @app.callback(
        Output('redirect','href', allow_duplicate=True),
        Input('device-delete-confirm-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def delete_device(n_clicks):
        if n_clicks:
            mac_address = session['selected_device_mac_address']
            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/device/delete/{mac_address}'
            try:
                response = requests.delete(api_url, verify=server["server"]["verify"])
                if response.status_code == 200:
                    return "/beha-pulse/main/device/"
                else:
                    return no_update
            except requests.exceptions.RequestException as e:
                return no_update
        else:
            return no_update
