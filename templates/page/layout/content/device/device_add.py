from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output

on_style = {'font-size': '1rem', 'align-items': 'center', 'cursor': 'pointer'}
off_style = {'font-size': '1rem', 'align-items': 'center', 'cursor': 'pointer'}


def add_row(icon_class, label, placeholder):
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

            html.Div([
                dcc.Input(type='text',
                          placeholder=placeholder,
                          id=f'device-add-input-{label}',
                          className='device-add-input'
                          )
            ], style={'display': 'inline-block', 'width': '80%', 'height': '7vh'},
            ),
        ], style={'display': 'flex', 'justify-content': 'start', 'align-items': 'center',
                  'padding': '10px 0px', 'width': '95%'},
    )


def add_on_off(icon_class, on_style, off_style):
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


def device_add_layout():
    layout = html.Div([
        dcc.Location(id='device-add', refresh=True),
        dbc.Container([
            # 상단 영역: 뒤로가기 아이콘과 타이틀
            html.Div([
                dbc.Row([
                    dbc.Col(
                        html.I(className='ic-arrow-back', id='device-add-back-button',
                               style={'font-size': '1.2rem', 'width': '1.5rem', 'height': '1.5rem',
                                      'cursor': 'pointer'},
                               ),
                        className="d-flex align-items-center justify-content-center",
                        width="auto",
                    ),
                    dbc.Col(
                        html.Span("장치 추가",
                                  style={'font-weight': 'bold', 'color': '#3F3F3F', 'font-size': '1.5rem',
                                         'justify-content': 'center', 'align-items': 'center',
                                         'display': 'flex'}),
                        className="d-flex align-items-center justify-content-center",
                        width="auto"
                    ),
                ], className="align-items-center mt-5 justify-content-center", )

            ],
                id='device-add-header-content',
                className="d-flex justify-content-start mx-3",
            ),

            dcc.Loading(
                id="loading-spinner",
                type="circle",  # 다른 스피너 유형을 원할 경우 변경 가능
                children=html.Div([
                    add_row('ic-manufacturing', '장치', '장치'),
                    add_row('ic-computer', 'MAC 주소', 'MAC 주소'),
                    add_row('ic-local-hospital', '설치 장소', '설치 장소'),
                    add_row('ic-location-on', '설치 위치', '설치 위치'),
                    add_row('ic-calendar-month', '점검 날짜', 'YYYY-MM-DD'),
                    add_on_off('ic-offline-bolt', on_style, off_style),
                    add_row('ic-display-settings', '노트', '메모'),
                    add_row('ic-person-device', '사용자', '', )
                ], id='device-add-main-content',
                    className="d-flex flex-column justify-content-center align-items-center my-3",
                    style={'height': '75vh'}),
            ),
            html.Div([
                dbc.Button([
                    # 아이콘과 텍스트를 버튼 안에 배치
                    html.I(className='ic-device-add me-1', style={'width': '2rem', 'height': '2rem'}),
                    html.Span("추가완료", style={'font-size': '1rem', 'font-weight': 'bold'})
                ], color="primary", id='device-add-save-button'),
            ], className='d-flex w-100 p-0', style={'justify-content': 'end'})
        ], className="d-flex flex-column w-100 flex-grow-1"),  # flex-grow-1을 사용해 상단과 중간 영역을 확장 가능하게 설정
    ], className="min-vh-100 d-flex flex-column bg-white")

    return layout
