from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output


def edit_click(icon_class, label, value, placeholder):
    # 상태에 따른 색상 설정
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
            # get_Input(label, value, placeholder),
            html.Div([
                html.Div(value,
                         id=f'device-edit-input-{label}',
                         className='device-edit-input', style={'display':'flex', 'align-items':'center'},
                         )
            ], style={'display': 'inline-block', 'width': '80%', 'height': '7vh'}, ),
        ], style={'display': 'flex', 'justify-content': 'start', 'align-items': 'center',
                  'padding': '10px 0px', 'width': '95%'}, n_clicks=0
    )


def edit_row(icon_class, label, value, placeholder):
    # 상태에 따른 색상 설정
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
            # get_Input(label, value, placeholder),
            html.Div([
                dcc.Input(type='text',
                          placeholder=placeholder,
                          id=f'device-edit-input-{label}',
                          value=value,
                          className='device-edit-input'
                          )
            ], style={'display': 'inline-block', 'width': '80%', 'height': '7vh'}, ),
        ], style={'display': 'flex', 'justify-content': 'start', 'align-items': 'center',
                  'padding': '10px 0px', 'width': '95%'},
    )


def edit_on_off(icon_class, on_style, off_style):
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
            html.Div([
                html.Div([
                    html.Span('ON', style=on_style,
                              id='on-button', n_clicks=0),
                    html.Span('OFF', style=off_style,
                              id='off-button', n_clicks=0),
                ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%'}),
            ], style={'display': 'flex', 'width': '80%', 'height': '7vh', 'align-items': 'center',
                      'padding': '0 10vh', 'font-size': '1rem'},
            ),
        ], style={'display': 'flex', 'justify-content': 'start', 'align-items': 'center',
                  'padding': '10px 0px', 'width': '95%'},
    )


def device_edit_layout():
    layout = html.Div([
        dcc.Location(id='device-edit', refresh=True),
        dcc.Store(id='device-edit-store', data={}),  # 데이터를 저장할 숨겨진 Store
        # 오버레이 배경
        html.Div(id='device-user-overlay-background', style={
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
        html.Div(id='device-user-overlay-container', children=[
            html.Div(
                style={
                    'background': '#fff',
                    'border-radius': '30px',
                    'drop-shadow': '0 4px 4px rgba(0, 0, 0, 0.25)',
                    'width': '40vh',
                    'margin': 'auto',
                    'padding': '20px',
                    'position': 'relative',
                    'textAlign': 'center'
                }, id='device-user-overlay-content')
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
                        html.I(className='ic-arrow-back', id='device-edit-back-button',
                               style={'font-size': '1.2rem', 'width': '1.5rem', 'height': '1.5rem',
                                      'cursor': 'pointer'},
                               ),
                        className="d-flex align-items-center justify-content-center",
                        width="auto",
                    ),
                    dbc.Col(
                        html.Span("장치 수정",
                                  style={'font-weight': 'bold', 'color': '#3F3F3F', 'font-size': '1.5rem',
                                         'justify-content': 'center', 'align-items': 'center',
                                         'display': 'flex'}),
                        className="d-flex align-items-center justify-content-center",
                        width="auto"
                    ),
                ], className="align-items-center mt-5 justify-content-center", )

            ],
                id='device-edit-header-content',
                className="d-flex justify-content-start mx-3",
            ),

            dcc.Loading(
                id="loading-spinner",
                type="circle",  # 다른 스피너 유형을 원할 경우 변경 가능
                children=html.Div([
                ], id='device-edit-main-content',
                    className="d-flex flex-column justify-content-center align-items-center my-3",
                    style={'height': '75vh', 'padding': '0px 20px'}),
            ),
            html.Div([
                dbc.Button([
                    # 아이콘과 텍스트를 버튼 안에 배치
                    html.I(className='ic-edit me-1', style={'width': '2rem', 'height': '2rem'}),
                    html.Span("수정하기", style={'font-size': '1rem', 'font-weight': 'bold'})
                ], color="primary", id='device-edit-save-button', href='/beha-pulse/main/device/edit/'),
            ], className='d-flex w-100 p-0', style={'justify-content': 'end'})
        ], className="d-flex flex-column w-100 flex-grow-1"),  # flex-grow-1을 사용해 상단과 중간 영역을 확장 가능하게 설정
    ], className="min-vh-100 d-flex flex-column bg-white")

    return layout
