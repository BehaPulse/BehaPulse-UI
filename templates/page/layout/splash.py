from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

from dash import html, dcc
import dash_bootstrap_components as dbc


def splash_layout():
    return html.Div([
        # 상단 로고 및 텍스트 영역
        dbc.Container(
            [
                dbc.Row(
                    html.Img(src="assets/img/favicon.svg", style={'width': '30vh', 'height': '30vh'}),
                    className='align-items-center justify-content-center'
                ),
                dbc.Row(
                    html.P(["와이파이 센싱으로 편안하고", html.Br(), "안전한 케어를 제공합니다"],
                           style={'color': '#3F3F3F', 'font-size': '1.2rem', 'text-align': 'center'}, ),
                    className="text-center my-3 justify-content-center"
                ),
            ],
            className="d-flex flex-column justify-content-center align-items-center flex-grow-1"
        ),

        # 하단 버튼 영역
        dbc.Container([
            dbc.Row(
                dbc.Button("시작하기", href="/beha-pulse/signup/",
                           style={
                               'font-size': '1.2rem',  # 폰트 크기 설정
                               'height': '50px',  # 버튼 높이 설정
                               'border-radius': '10px',  # 모서리 둥글기 설정
                               'text-align': 'center',  # 텍스트 가로 정렬 (중앙)
                               'display': 'flex',  # Flexbox 사용
                               'justify-content': 'center',  # Flexbox로 가로 가운데 정렬
                               'align-items': 'center'  # Flexbox로 세로 가운데 정렬
                           }),
                className='justify-content-center my-3 align-items-center w-100'
            ),
            dbc.Row(
                [
                    html.P([
                        html.Span("이미 계정이 있으신가요?", style={'color': '#C8C8C8'}),
                        html.A("로그인", href="/beha-pulse/login/", style={'color': '#003CFF', 'margin-left': '10px',
                                                                        'text-decoration': 'none'})
                    ], className="text-center p-0 m-0"),
                ],
                className="justify-content-center align-items-center w-100"
            )
        ],
            className="d-flex flex-column align-items-center justify-content-end flex-grow-0 pb-3 w-100 my-3")
    ], className="min-vh-100 d-flex flex-column bg-white")
