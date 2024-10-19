from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output
import dash_daq as daq


def control_color_layout():
    layout = html.Div([
        dbc.Container([
            # 상단 영역: 뒤로가기 아이콘과 타이틀
            html.Div([
                dbc.Row([
                    dbc.Col(
                        html.I(className='ic-arrow-back', id='control-color-back-button',
                               style={'font-size': '1.2rem', 'width': '1.5rem', 'height': '1.5rem',
                                      'cursor': 'pointer'},
                               ),
                        className="d-flex align-items-center justify-content-center",
                        width="auto",
                    ),
                    dbc.Col(
                        html.Span("조명 관리",
                                  style={'font-weight': 'bold', 'color': '#3F3F3F', 'font-size': '1.5rem',
                                         'justify-content': 'center', 'align-items': 'center',
                                         'display': 'flex'}),
                        className="d-flex align-items-center justify-content-center",
                        width="auto"
                    ),
                ], className="align-items-center mt-4 mb-3 justify-content-center", )

            ],
                className="d-flex justify-content-start mx-3",
            ),
        ]),

        dbc.Container([
            dcc.Loading(
                id="loading-spinner",
                type="circle",
                children=html.Div(children=control_content(), id='main-content', className='d-flex w-100 h-100')
            )
        ],className='flex-grow-1')

    ], className="min-vh-100 d-flex flex-column bg-white")

    return layout


def control_content():
    content = html.Div([
        dcc.Store(id='color-data-store', data={}),  # 데이터를 저장할 숨겨진 Store

        # Brightness Slider
        html.Div([
            html.Div([
                html.Span(className='ic-light-left', style={'margin-right': '10px', 'width': '5vh', 'height': '5vh'}),

                dcc.Slider(id='brightness-slider',
                           min=0,
                           max=100,
                           value=50,
                           marks={0: '', 100: ''},  # 빈 공간으로 양쪽 마크
                           step=1,
                           tooltip={'placement': 'bottom', 'always_visible': False},
                           updatemode='drag',  # 슬라이더를 드래그할 때 업데이트
                           className="flex-grow-1 p-0",
                           ),  # 슬라이더가 영역을 차지하게 함),
                html.Span(className='ic-light-right', style={'margin-left': '10px', 'width': '5vh', 'height': '5vh'}),

            ], style={'background': '#EEEEEE', 'border-radius': '25px', 'transform: ': 'matrix(-1, 0, 0, 1, 0, 0)',
                      'justify-content': 'space-between',
                      'width': '100%', 'height': '7vh', 'display': 'flex', 'align-items': 'center',
                      'padding': '0 20px'}),
        ], style={'margin-bottom': '20px', 'width': '100%'}),

        # Create canvas for color wheel
        html.Canvas(id='colorWheelCanvas', style={'border-radius': '50%', 'cursor': 'pointer', 'margin-top':'5vh'},
                    width=300, height=300),

        dbc.Row([
            html.Div(
                [
                    html.I(id='colorDisplay', style={'width': '4vh', 'height': '4vh', 'border-radius': '50%', 'background': '#FFFFFF'}),
                    html.Span(style={'font-size': '1rem'}, id='selectedColor'),
                    html.I(style={'width': '4vh', 'height': '4vh'}),
                ]
                , style={'background': '#FFFFFF', 'box-shadow': '0px 0px 17px 2px rgba(0, 0, 0, 0.13)',
                         'border-radius': '15px', 'width': '80%', 'height': '7vh', 'display': 'flex',
                         'align-items': 'center', 'justify-content': 'space-between'}
            )
        ], className="w-100 p-0", style={'margin-top': '5vh', 'display': 'flex', 'justify-content': 'center', 'margin-bottom': '2vh'}),


        dbc.Container([
            dbc.Row(
                dbc.Button("저장하기",
                           id='control-color-save-button',
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
            )], className="d-flex flex-column align-items-center justify-content-end flex-grow-0 w-100"

        ),

    ], className="d-flex align-items-center flex-column mx-3 w-100 justify-content-center h-100")
    return content
