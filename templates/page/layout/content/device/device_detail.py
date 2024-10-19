from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output


# 재사용 가능한 장치 항목 컴포넌트 함수
def info_row(icon_class, label, value, status=None):
    """장치 항목 컴포넌트"""
    # 상태에 따른 색상 설정
    if status == "ON":
        value_color = "#00D84F"
        font_weight = 'bold'  # 녹색
    elif status == "OFF":
        value_color = "#E10000"  # 빨간색
        font_weight = 'bold'
    else:
        value_color = "#9C9C9C"  # 기본 색상 (회색)
        font_weight = 'normal'

    return html.Div(
        [
            # 왼쪽 아이콘
            html.Div([
                html.I(className=icon_class, style={'height': '5vh', 'width': '5vh'}),
            ], style={'display': 'flex', 'background-color': '#EEEEEE',
                      'justify-content': 'center', 'align-items': 'center',
                      'border-radius': '10px', 'width': '7vh', 'height': '7vh',
                      'margin-right': '20px'
                      },
            ),
            # 중앙 라벨
            html.Div([
                html.Span(label, style={'font-size': '1rem'}),
            ], style={'display': 'inline-block', 'width': '25%'}),

            # 오른쪽 값
            html.Div([
                html.Span(value, style={'color': value_color, 'font-size': '1rem', 'font-weight': font_weight}),
            ], style={'display': 'inline-block', 'width': '55%', 'text-align': 'center'}),

        ], style={'display': 'flex', 'justify-content': 'start', 'align-items': 'center',
                  'padding': '10px 0px', 'width': '95%'},
    )


def device_detail_layout():
    layout = html.Div([
        dcc.Location(id='device-detail', refresh=True),

        # 오버레이 배경
        html.Div(id='device-overlay-background', style={
            'display': 'none',
            'position': 'fixed',
            'top': 0,
            'left': 0,
            'width': '100%',
            'height': '100%',
            'backgroundColor': 'rgba(0, 0, 0, 0.4)',
            'zIndex': 1
        }),

        # 오버레이 팝업 창
        html.Div(id='device-delete-overlay-container', children=[
            html.Div([
                html.Div(style={'font-size': '18px', 'padding': '10px', 'cursor': 'pointer'}, id='device-delete-overlay-text'),
                html.Div([
                    html.Div([
                        html.Div("확인", style={'font-size': '18px', 'padding': '10px', 'cursor': 'pointer',
                                              'background': '#003CFF', 'width': '40%', 'border-radius': '8px',
                                              'color': '#fff'},
                                 id='device-delete-confirm-button'),
                        html.Div("취소", style={'font-size': '18px', 'padding': '10px', 'cursor': 'pointer',
                                              'background': '#D5D5D5', 'width': '40%', 'border-radius': '8px',
                                              'color': '#fff'},
                                 id='device-delete-cancel-button')
                    ], style={'display': 'flex', 'width': '90%', 'justify-content': 'space-around'}),
                ],
                    style={'display': 'flex', 'width': '100%', 'justify-content': 'center', 'margin-top': '20px'},
                )
            ], style={
                'background': '#fff',
                'border-radius': '30px',
                'drop-shadow': '0 4px 4px rgba(0, 0, 0, 0.25)',
                'width': '40vh',
                'margin': 'auto',
                'padding': '20px',
                'position': 'relative',
                'textAlign': 'center'
            }, id='device-delete-overlay-content')
        ], style={
            'display': 'none',
            'position': 'fixed',
            # 'top': '10vh',
            # 'left': '5vw',
            # 'transform': 'translate(-10vw, -10vh)',
            'top': '50%',
            'left': '50%',
            'transform': 'translate(-50%, -50%)',
            'zIndex': 2
        }),

        dbc.Container([
            # 상단 영역: 뒤로가기 아이콘과 타이틀
            html.Div([
                dbc.Row([
                    dbc.Col(
                        html.I(className='ic-arrow-back', id='device-detail-back-button',
                               style={'font-size': '1.2rem', 'width': '1.5rem', 'height': '1.5rem',
                                      'cursor': 'pointer'},
                               ),
                        className="d-flex align-items-center justify-content-center",
                        width="auto",
                    ),
                    dbc.Col(
                        html.Span("장치 정보",
                                  style={'font-weight': 'bold', 'color': '#3F3F3F', 'font-size': '1.5rem',
                                         'justify-content': 'center', 'align-items': 'center',
                                         'display': 'flex'}),
                        className="d-flex align-items-center justify-content-center",
                        width="auto"
                    ),
                ], className="align-items-center mt-5 justify-content-center", )

            ],
                id='device-detail-header-content',
                className="d-flex justify-content-start mx-3",
            ),

            dcc.Loading(
                id="loading-spinner",
                type="circle",  # 다른 스피너 유형을 원할 경우 변경 가능
                children=html.Div(id='device-detail-main-content',
                                  className="d-flex flex-column justify-content-center align-items-center my-3",
                                  style={'height': '75vh', 'padding':'0px 20px'}),
            ),
            html.Div([
                dbc.Button([
                    # 아이콘과 텍스트를 버튼 안에 배치
                    html.I(className='ic-edit me-1', style={'width': '2rem', 'height': '2rem'}),
                    html.Span("수정하기", style={'font-size': '1rem', 'font-weight': 'bold'})
                ], color="primary", id='device-edit-button', href='/beha-pulse/main/device/edit/'),
                dbc.Button([
                    # 아이콘과 텍스트를 버튼 안에 배치
                    html.I(className='ic-delete me-1', style={'width': '2rem', 'height': '2rem'}),
                    html.Span("삭제하기", style={'font-size': '1rem', 'font-weight': 'bold'})
                ], color="danger", id='device-delete-button')
            ], className='d-flex w-100 p-0', style={'justify-content': 'space-between'})
        ], className="d-flex flex-column w-100 flex-grow-1"),  # flex-grow-1을 사용해 상단과 중간 영역을 확장 가능하게 설정
    ], className="min-vh-100 d-flex flex-column bg-white")

    return layout
