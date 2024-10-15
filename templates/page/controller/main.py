from app import admin_app
from flask import Flask, session
from dash import Dash, dcc, html, callback_context, no_update
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import requests


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
