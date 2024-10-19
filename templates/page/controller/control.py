from dash.exceptions import PreventUpdate

from app import admin_app
from flask import Flask, session
from dash import Dash, dcc, html, callback_context, no_update
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
import requests
import json
from datetime import datetime

from ..layout.content.control.control import *

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


def hex_to_rgba_and_shadow(hex_value, alpha=0.5, x_offset=0, y_offset=0, blur_radius=50, spread_radius=20):
    # Strip the hash (#) if present
    hex_value = hex_value.lstrip('#')
    # Convert hex to RGB
    r, g, b = tuple(int(hex_value[i:i + 2], 16) for i in (0, 2, 4))
    # Return formatted rgba and box-shadow style string
    return f"rgba({r}, {g}, {b}, {alpha}) {x_offset}px {y_offset}px {blur_radius}px {spread_radius}px"


def control_controller(app):
    @app.callback(
        Output('redirect', 'pathname', allow_duplicate=True),
        Input('control-back-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def back_to_main(n_clicks):
        if n_clicks:
            return '/beha-pulse/main/control/'

    @app.callback(
        Output('control-rows', 'children'),
        Input('url', 'pathname')
    )
    def set_dashboard_list_row(pathname):
        if pathname == '/beha-pulse/main/control/':
            control_row = []
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
                        control_list = response.json().get('dashboards', [])
                        for control in control_list:
                            if control['personId'] in person_id_list:
                                control_row.append(control_item(
                                    control['personId'],
                                    control['name'],
                                    control['gender'],
                                    control['birth'],
                                ))
                else:
                    control_row.append(no_row_item(initial=True))
                    return [html.Div(control_row, style={'width': '100%', 'height': '100%',
                                                           'display': 'flex', 'align-itmes': 'center',
                                                           'justify-content': 'center'})]

            except Exception as e:
                control_row.append([])

            return [html.Div(control_row)]


    @app.callback(
        Output('redirect', 'pathname', allow_duplicate=True),
        Input({'type': 'control-row', 'index': ALL}, 'n_clicks'),
        prevent_initial_call=True
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
            session['person_id'] = clicked_id
            return '/beha-pulse/main/control/setting/'

    @app.callback(
        Output('redirect', 'pathname', allow_duplicate=True),
        [Input('control-lying-down', 'n_clicks'),
         Input('control-empty-down', 'n_clicks'),
         Input('control-sitting-down', 'n_clicks')],
        prevent_initial_call=True
    )
    def control_data_store(lying_down, empty_down, sitting_down):
        if lying_down:
            session['setting_person_status'] = '누워있음'
            return '/beha-pulse/main/control/color/'
        elif empty_down:
            session['setting_person_status'] = '비어있음'
            return '/beha-pulse/main/control/color/'
        elif sitting_down:
            session['setting_person_status'] = '앉아있음'
            return '/beha-pulse/main/control/color/',
        else:
            return no_update

    @app.callback(
        Output('redirect', 'pathname', allow_duplicate=True),
        [Input('control-color-back-button', 'n_clicks')],
        prevent_initial_call=True
    )
    def back_to_control(n_clicks):
        if n_clicks:
            return '/beha-pulse/main/control/setting/'

    app.clientside_callback(
        '''
        function(_, _, storeData) {
            const canvas = document.getElementById('colorWheelCanvas');
            const ctx = canvas.getContext('2d');
            const colorDisplay = document.getElementById('colorDisplay');
            const selectedColorText = document.getElementById('selectedColor');
            let returnColor = '';
            
            if (!storeData) {
                storeData = {};
            }
            
            
            // 원형 색상 휠을 그리는 함수
            function drawColorWheel() {
                const radius = canvas.width / 2;
                const gradient = ctx.createConicGradient(0, radius, radius);
                gradient.addColorStop(0, 'red');
                gradient.addColorStop(1 / 6, 'yellow');
                gradient.addColorStop(2 / 6, 'lime');
                gradient.addColorStop(3 / 6, 'cyan');
                gradient.addColorStop(4 / 6, 'blue');
                gradient.addColorStop(5 / 6, 'magenta');
                gradient.addColorStop(1, 'red');

                ctx.fillStyle = gradient;
                ctx.beginPath();
                ctx.arc(radius, radius, radius, 0, 2 * Math.PI);
                ctx.fill();
            }

            // RGB를 Hex로 변환하는 함수
            function rgbToHex(r, g, b) {
                return `#${((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1).toUpperCase()}`;
            }

            // 캔버스에서 클릭한 위치의 색상 가져오기
            canvas.addEventListener('click', function (e) {
                const rect = canvas.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

                const pixel = ctx.getImageData(x, y, 1, 1).data;
                const hexColor = rgbToHex(pixel[0], pixel[1], pixel[2]);

                colorDisplay.style.backgroundColor = hexColor;
                selectedColorText.textContent = `${hexColor}`;
                console.log(selectedColorText.textContent);
                returnColor = selectedColorText.textContent;
                storeData['color'] = returnColor;
            });

            // 원형 색상 휠 그리기
            drawColorWheel();
            
            return [storeData];
        }
        ''',
        Output('color-data-store', 'data'),  # 더미 Output, 값이 필요하지 않지만 콜백을 실행하기 위함
        Input('colorWheelCanvas', 'id'),  # 더미 Input, DOM 로딩 후 실행을 보장하기 위한 용도
        Input('colorDisplay', 'id'),  # 더미 Input, 동일한 이유로 추가
        State('color-data-store', 'data'),  # 데이터를 저장할 Store
    )

    @app.callback(
        [Output('redirect', 'pathname', allow_duplicate=True),
         Output('selectedColor', 'children', allow_duplicate=True),
         ],
        Input('control-color-save-button', 'n_clicks'),
        [State('color-data-store', 'data'),
         State('brightness-slider', 'value')
         ], prevent_initial_call=True
    )
    # 세이브 버튼을 눌렀을 때, 색을 저장
    #
    # case 1. 색이 선택되지 않았을 때,
    #     a. 근데 기존의 유저가 선택했던 정보가 존재한다. -> 기존의 정보를 가져와서 업데이트
    #     b. 근데 기존의 유저가 선택했던 정보가 존재하지 않는다. -> 색을 선택하지 않았다고 출력
    #
    # case 2. 색이 선택되었을 때,
    #     a. 근데 기존의 유저가 선택했던 정보가 존재한다. -> 색을 정보를 업데이트
    #     b. 근데 기존의 유저가 선택했던 정보가 존재하지 않는다. -> 색을 저장

    def save_color(n_clicks, color, brightness):
        if n_clicks:
            color = color.pop().get('color')

            # case 1
            if color is None:
                api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/color_brightness/{session["person_id"]}/{session["setting_person_status"]}'
                try:
                    response = requests.get(api_url, verify=server["server"]["verify"])
                    if response.status_code == 200:
                        color_brightness = response.json().get('colorBrightness')

                        # case 1-a
                        if color_brightness:
                            color = color_brightness[0].get('color')
                            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/color_brightness/update/{color_brightness[0].get("id")}'
                            data = {
                                'color': color,
                                'brightness': brightness,
                                'status': session.get('setting_person_status'),
                                'personId': session.get('person_id')
                            }
                            response = requests.put(api_url, json=data, verify=server["server"]["verify"])

                            if response.status_code == 200:
                                return '/beha-pulse/main/control/setting/', ""
                            elif response.status_code == 404 and response.json().get(
                                    'message') == 'ColorBrightness entry not found.':
                                return no_update, "색이 변경되지 않았습니다."
                            else:
                                return no_update, ""

                        # case 1-b
                        else:
                            return no_update, "색이 선택되지 않았습니다."
                    else:
                        return no_update, ""
                except Exception as e:
                    return no_update, ""

            # case 2
            else:
                api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/color_brightness/{session["person_id"]}/{session["setting_person_status"]}'
                try:
                    response = requests.get(api_url, verify=server["server"]["verify"])
                    if response.status_code == 200:
                        color_brightness = response.json().get('colorBrightness')

                        # case 2-a
                        if color_brightness:
                            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/color_brightness/update/{color_brightness[0].get("id")}'
                            data = {
                                'color': color,
                                'brightness': brightness,
                                'status': session.get('setting_person_status'),
                                'personId': session.get('person_id')
                            }
                            response = requests.put(api_url, json=data, verify=server["server"]["verify"])

                            if response.status_code == 200:
                                return '/beha-pulse/main/control/setting/', ""
                            else:
                                return no_update, ""

                        # case 2-b
                        else:
                            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/color_brightness/register'
                            data = {
                                'color': color,
                                'brightness': brightness,
                                'status': session.get('setting_person_status'),
                                'personId': session.get('person_id')
                            }
                            response = requests.post(api_url, json=data, verify=server["server"]["verify"])

                            if response.status_code == 200:
                                return '/beha-pulse/main/control/setting/', ""
                            else:
                                return no_update, ""
                    else:
                        return no_update, ""
                except Exception as e:
                    return no_update, ""

        else:
            return no_update, ""

    @app.callback(
        [Output('colorDisplay', 'style'),
         Output('selectedColor', 'children'),
         Output('brightness-slider', 'value')
         ],
        Input('url', 'pathname'),
        State('colorDisplay', 'style'),
    )
    def set_color_content(pathname, display_style):
        if pathname == '/beha-pulse/main/control/color/':
            personId = session.get('person_id')
            status = session.get('setting_person_status')
            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/color_brightness/{personId}/{status}'
            try:
                response = requests.get(api_url, verify=server["server"]["verify"])
                if response.status_code == 200:
                    color_brightness = response.json().get('colorBrightness', [])
                    if color_brightness:
                        color = color_brightness[0].get('color')
                        brightness = color_brightness[0].get('brightness')
                        display_style['backgroundColor'] = color
                        return [display_style, color, brightness]
                    else:
                        return [display_style, '', 50]
                else:
                    return [display_style, '', 50]
            except Exception as e:
                return [display_style, '', 50]

        return [display_style, '', 50]

    @app.callback(
        [Output('contorl_setting_circle', 'style'),
         Output('control-setting-now-status', 'children'),
         Output('control-setting-now-status', 'style'),
         Output('ic-schedule', 'style')
         ],
        Input('url', 'pathname'),
        [State('contorl_setting_circle', 'style'),
         State('control-setting-now-status', 'style'),
         State('ic-schedule', 'style')
         ],
    )
    def set_circle_content(pathname, circle_style, text_style, ic_schedule_style):
        if pathname == '/beha-pulse/main/control/setting/':
            personId = session.get('person_id')
            # 사용자 상태부터 확인
            api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/dashboard/{personId}'
            try:
                response = requests.get(api_url, verify=server["server"]["verify"])
                if response.status_code == 200:
                    # 사용자 정보
                    dashboard = response.json().get('dashboard', [])
                    if dashboard:
                        # 현재 상태만 가져오기
                        now_status = dashboard.get('status')
                        if now_status == None:
                            return no_update, "정보 없음", no_update, no_update
                        # 현재 상태를 바탕으로 색상 및 밝기 가져오기
                        api_url = f'{server["server"]["protocol"]}://{server["server"]["host"]}:{server["server"]["port"]}/color_brightness/{personId}/{now_status}'
                        response = requests.get(api_url, verify=server["server"]["verify"])

                        if response.status_code == 200:
                            color_brightness = response.json().get('colorBrightness', [])
                            if color_brightness:
                                color = color_brightness[0].get('color')
                                circle_style['backgroundColor'] = color
                                circle_style['boxShadow'] = hex_to_rgba_and_shadow(color)
                                text_style['color'] = color

                                # 현재 상태에 따라 아이콘 변경
                                background_image = ic_schedule_style['background-image']
                                start_index = background_image.find("fill='") + len("fill='")
                                end_index = background_image.find("'", start_index)
                                color = color.replace('#', '%23')
                                background_image = background_image[:start_index] + color + background_image[end_index:]
                                ic_schedule_style['background-image'] = background_image
                                return circle_style, now_status, text_style, ic_schedule_style

                            elif not color_brightness:
                                return no_update, now_status, no_update, no_update
                        else:
                            return no_update, now_status, no_update, no_update
                    else:
                        return no_update, "정보 없음", no_update, no_update
                else:
                    return no_update, "정보 없음", no_update, no_update

            except Exception as e:
                return no_update, "정보 없음", no_update, no_update
        else:
            return no_update, "정보 없음", no_update, no_update
