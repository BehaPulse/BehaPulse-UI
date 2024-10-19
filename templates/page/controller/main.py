from dash.exceptions import PreventUpdate

from app import admin_app
from flask import Flask, session
from dash import Dash, dcc, html, callback_context, no_update
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
import requests
import json

with open('config/server.json', 'r') as f:
    server = json.load(f)


def overlay_item(label):
    return html.Div(label, style={'font-size': '18px', 'padding': '10px', 'cursor': 'pointer'},
                    id={'type': 'overlay_location', 'index': label},  # 각 줄에 고유 id 부여
                    )


# Callback을 통해 버튼 클릭 시 이동하는 경로 설정
def main_bottom_controller(app):
    @app.callback(
        Output('redirect', 'pathname'),
        [Input('main-home-button', 'n_clicks'),
         Input('main-device-button', 'n_clicks'),
         Input('main-control-button', 'n_clicks'),
         Input('main-dashboard-button', 'n_clicks'),
         Input('main-more-button', 'n_clicks')]
    )
    def navigate_to_page(home, device, control, dashboard, more):
        ctx = callback_context  # 현재 클릭한 버튼을 확인하기 위한 context

        # 아무 버튼도 클릭되지 않았다면 업데이트 없음
        if not ctx.triggered:
            return no_update

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]  # 클릭된 버튼의 ID 가져오기
        # 버튼이 눌렸을 때
        if home or device or control or dashboard or more:
            # 버튼 ID에 따라 경로 반환
            if button_id == 'main-home-button':  # 홈 버튼 클릭 시 이동
                return '/beha-pulse/main/'
            elif button_id == 'main-device-button':  # 장치 버튼 클릭 시 이동
                return '/beha-pulse/main/device/'
            elif button_id == 'main-control-button':  # 대시보드 버튼 클릭 시 이동
                return '/beha-pulse/main/control/'
            elif button_id == 'main-dashboard-button':  # 유저 버튼 클릭 시 이동
                return '/beha-pulse/main/dashboard/'
            elif button_id == 'main-more-button':
                return '/beha-pulse/main/more/'

        return no_update  # 업데이트 없음

    @app.callback(
        [Output('overlay-background', 'style'),
         Output('overlay-container', 'style')],
        [Input('main-down-button', 'n_clicks'),
         Input('overlay-background', 'n_clicks')],
        [State('overlay-background', 'style'),
         State('overlay-container', 'style')]
        , prevent_initial_call=True
    )
    def toggle_overlay(n_clicks_button, n_clicks_background, background_style, container_style):
        # 팝업을 켜는 경우
        ctx = callback_context
        if not ctx.triggered:
            return background_style, container_style
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        # 버튼 클릭으로 열기
        if triggered_id == 'main-down-button' and n_clicks_button:
            background_style['display'] = 'block'
            container_style['display'] = 'block'
        # 오버레이 클릭으로 닫기
        elif triggered_id == 'overlay-background' and n_clicks_background:
            background_style['display'] = 'none'
            container_style['display'] = 'none'
        return background_style, container_style

    @app.callback(
        [Output('main-sensitivity-lying-slider', 'value'),
         Output('main-sensitivity-empty-slider', 'value'),
         Output('main-sensitivity-sitting-slider', 'value')],
        Input('url', 'pathname'),
    )
    def set_sensitivity_slider_value(pathname):
        lying, empty, sitting = 1, 1, 1
        if pathname == '/beha-pulse/main/sensitivity/':
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
        Input('main-sensitivity-save-button', 'n_clicks'),
        [State('main-sensitivity-lying-slider', 'value'),
         State('main-sensitivity-empty-slider', 'value'),
         State('main-sensitivity-sitting-slider', 'value'),
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
                            # if add_response.status_code == 201:
                            #     print(f'{status} 상태의 민감도가 새로 등록되었습니다.')
                            # else:
                            #     print(f'{status} 상태의 민감도 등록에 실패했습니다. 코드: {add_response.status_code}')

                        elif old_sensitivities[status] != new_weight:
                            # Case 2: 민감도가 존재하지만 값이 변경되었으면 업데이트
                            update_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/sensitivity/update/{session["user_id"]}/{status}'
                            data = {
                                'userEmail': session["user_id"],
                                'targetStatus': status,
                                'weight': new_weight
                            }

                            update_response = requests.put(update_url, json=data, verify=server["server"]["verify"])

                            # if update_response.status_code == 200:
                            #     # return '/beha-pulse/main/sensitivity/'
                            #     print(f'{status} 상태의 민감도가 업데이트되었습니다.')
                            # else:
                            #     print(f'{status} 상태의 민감도 업데이트에 실패했습니다. 코드: {update_response.status_code}')

                        # else:
                        #     # Case 3: 변경되지 않은 경우 업데이트하지 않음
                        #     print(f'{status} 상태의 민감도는 변경되지 않았습니다.')

                        api_count += 1

                    if api_count == len(new_sensitivities):
                        return '/beha-pulse/main/sensitivity/'

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
                                return '/beha-pulse/main/sensitivity/'
                else:
                    return no_update
            except requests.exceptions.RequestException as e:
                # return 1, 1, 1
                return no_update
        return no_update

    @app.callback(
        Output('redirect', 'href', allow_duplicate=True),
        Input('main-back-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def back_to_main(n_clicks):
        if n_clicks:
            return '/beha-pulse/main/'
        return no_update

    @app.callback(
        Output('redirect', 'pathname', allow_duplicate=True),
        Input('main-sensitivity-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def navigate_to_sensitivity(n_clicks):
        if n_clicks:
            return '/beha-pulse/main/sensitivity/'
        return no_update

    @app.callback(
        Output('main-user-name', 'children'),
        Input('url', 'pathname'),
    )
    def set_user_name(pathname):
        if pathname == '/beha-pulse/main/':
            return session['user_name']
        return no_update

    @app.callback(
        [Output('main-location', 'children'),
         Output('overlay-content', 'children'), ],
        Input('url', 'pathname'),
    )
    # 장치가 설치된 장소를 기반으로 메인 화면에서 장소를 선택할 수 있도록 설정
    # 장치가 만일 존재한다면 -> 장치가 설치된 장소를 가져와서 overlay에 표시
    # 장치가 존재하지 않는다면 -> overlay에 표시할 장소가 없음 -> 표시 X
    def set_overlay_value(pathname):
        print(pathname)
        # if pathname == '/beha-pulse/main/':
        api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/user_device/user_devices_with_location/{session["user_id"]}'
        try:
            response = requests.get(api_url, verify=server["server"]["verify"])

            # 디바이스가 설치된 장소가 존재
            if response.status_code == 200:
                location = response.json().get('location')
                location = ["장소 미설정" if item == "" else item for item in location]

                location.sort()

                session['location'] = location

                # 선택된 위치가 없을 경우 첫 번째 위치 선택
                if 'selected_location' not in session or not session['selected_location']:
                    session['selected_location'] = location[0]

                location_overlay = []
                for loc in location:
                    location_overlay.append(overlay_item(loc))

                return session['selected_location'], html.Div(location_overlay)

            # 디바이스가 설치된 장소가 존재하지 않음
            elif response.status_code == 404:
                session['location'] = ['장소 미설정']
                session['selected_location'] = '장소 미설정'

                return session['selected_location'], html.Div('장소 미설정')
            else:
                return no_update
        except requests.exceptions.RequestException as e:
            return no_update
        # return no_update

    @app.callback(
        Output('redirect', 'href', allow_duplicate=True),
        Input({'type': 'overlay_location', 'index': ALL}, 'n_clicks'),
        State('url', 'pathname'),
        prevent_initial_call=True
    )
    def set_selected_location(n_clicks, url):
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
            session['selected_location'] = clicked_id
            return url

        return no_update

    @app.callback(
        Output('main-device-count', 'children'),
        Input('url', 'pathname'),
    )
    def set_device_count(pathname):
        if pathname == '/beha-pulse/main/':
            count = 0
            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/user_device/user_devices_with_details/{session["user_id"]}'
            try:
                response = requests.get(api_url, verify=server["server"]["verify"])
                if response.status_code == 200:
                    device_list = response.json().get('user_devices')

                    if 'selected_location' not in session or not session['selected_location']:
                        session['selected_location'] = device_list[0]['location']
                        return f"현재 {len(device_list)}개의 장치를 관리하고 있습니다."

                    for device in device_list:
                        if device['location'] == '':
                            device['location'] = '장소 미설정'
                        if device['location'] == session['selected_location']:
                            count += 1

                    return f"현재 {count}개의 장치를 관리하고 있습니다."
                elif response.status_code == 404:
                    return f"현재 {0}개의 장치를 관리하고 있습니다."
                else:
                    return no_update
            except requests.exceptions.RequestException as e:
                return no_update
        return no_update

    @app.callback(
        Output('profile-image', 'src'),
        Input('url', 'pathname'),
    )
    def set_profile_image(pathname):
        if pathname == '/beha-pulse/main/':
            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/user/{session["user_id"]}'
            try:
                response = requests.get(api_url, verify=server["server"]["verify"])
                if response.status_code == 200:
                    user = response.json().get('user')
                    if user['gender'] == 'male':
                        return '../assets/img/man_profile.svg'
                    else :
                        return '../assets/img/girl_profile.svg'

                else:
                    return no_update
            except requests.exceptions.RequestException as e:
                return no_update
        return no_update
