from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


def login_layout():
    layout = html.Div([
        dcc.Location(id='login', refresh=True),  # 페이지 이동을 위한 Location
        dcc.Store(id='login-result-store'),  # 로그인 결과를 저장할 Store
        html.Div(id='dummy-output', style={'display': 'none'}),  # Dummy Output 추가
        # 상단 텍스트 영역
        dbc.Container(
            [
                html.P(["안녕하세요", html.Br(), "BehaPulse입니다."],
                       style={'font-size': '2rem', 'color': '#3F3F3F',
                              'margin-bottom': '3vh'},

                       ),
                html.P("회원 서비스를 위해 로그인을 해주세요.",
                       style={'color': '#3F3F3F', 'font-size': '1rem', 'margin-bottom': '4vh'},
                       className='mx-3'
                       ),
                dbc.Input(placeholder="아이디 입력", type="text", id="login-email", className='login-input'),
                dbc.Input(placeholder="비밀번호 입력", type="password", id="login-password", className='login-input'),

            ], className="d-flex flex-column justify-content-center flex-grow-1 p-4"
        ),
        # 높이 조절을 위한 빈 컨테이너
        dbc.Container(className='flex-grow-1'),
        # 로그인 버튼 및 하단 텍스트
        dbc.Container([
            # 로그인 버튼
            dbc.Button("로그인", id="login-button", color="primary", className='w-100',
                       style={'height': '50px', 'border-radius': '7px', 'font-size': '1.25rem', 'margin-bottom': '1vh'}),
            # 하단 텍스트
            html.Div([
                html.A("아이디 찾기", href="/beha-pulse/find-id/", style={'text-decoration': 'none', 'color': '#000000'}),
                # 첫 번째 구분선
                html.Div(style={
                    'border-left': '1px solid #c5c5c5',  # 세로 구분선 스타일
                    'height': '14px',
                    'margin': '0 10px'
                }),
                html.A("비밀번호 찾기", href="/beha-pulse/find-password/", style={'text-decoration': 'none', 'color': '#000000'}),
                # 두 번째 구분선
                html.Div(style={
                    'border-left': '1px solid #c5c5c5',
                    'height': '14px',
                    'margin': '0 10px'
                }),
                html.A("회원가입", href="/beha-pulse/signup/", style={'text-decoration': 'none', 'color': '#000000'}),
            ], className='d-flex justify-content-between align-items-center w-80 mt-1')

        ], className='d-flex flex-column justify-content-center align-items-center flex-grow-0 pb-3 w-100 my-3'),

    ], className="min-vh-100 d-flex flex-column bg-white align-items-center",
    )

    return layout
