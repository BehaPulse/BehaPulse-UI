from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


# Define the layout
def more_password_change_layout():
    layout = html.Div([
        dcc.Store(id='more-password-data-store', data={}),  # 데이터를 저장할 숨겨진 Store
        dcc.Location(id='more-password', refresh=True),  # 페이지 이동을 위한 Location
        dcc.Store(id='more-password-current-step-store', data=1),  # 현재 단계를 추적할 Store

        dbc.Container([
            # 상단 영역: 뒤로가기 아이콘과 타이틀
            html.Div([
                dbc.Row([
                    dbc.Col(
                        html.I(className='ic-arrow-back', id='more-password-back-button',
                               style={'font-size': '1.2rem', 'width': '1.5rem', 'height': '1.5rem',
                                      'cursor': 'pointer'},
                               ),
                        className="d-flex align-items-center justify-content-center",
                        width="auto",
                    ),
                    dbc.Col(
                        html.Span("비밀번호 변경",
                                  style={'font-weight': 'bold', 'color': '#3F3F3F', 'font-size': '1.5rem',
                                         'justify-content': 'center', 'align-items': 'center',
                                         'display': 'flex'}),
                        className="d-flex align-items-center justify-content-center",
                        width="auto"
                    ),
                ], className="align-items-center my-5 justify-content-center", )

            ],
                className="d-flex justify-content-start mx-3",
            ),
            # 중간 영역: 설명 텍스트
            html.Div([

            ],
                className="d-flex flex-column justify-content-center mx-5 mt-5",
                id='more-password-text-content'
            ),

            # 하단 영역: 입력 필드
            html.Div([
            ],
                className="d-flex flex-column justify-content-center align-items-center my-2",
                id='more-password-main-content'
            )
        ], className="d-flex flex-column w-100 flex-grow-1"),  # flex-grow-1을 사용해 상단과 중간 영역을 확장 가능하게 설정

        dbc.Container([
            dbc.Row(
                dbc.Button("다음",
                           id='more-password-next-button',
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
            )], className="d-flex flex-column align-items-center justify-content-end flex-grow-0 pb-3 w-100"

        ),

    ], className="min-vh-100 d-flex flex-column bg-white")

    return layout


def get_step_content_more_password(step):
    if step == 1:
        return more_password_step_1_content()
    elif step == 2:
        return more_password_step_2_content()
    elif step == 3:
        return more_password_final_content()
    elif step == 4:
        return more_password_error_content()
    else:
        return "Unknown Step", ""


def more_password_step_1_content():
    middle_content = dbc.Row(
        html.P(["기존 비밀번호를", html.Br(), "입력해주시길 바랍니다."],
               className='more-password-text-content-value'),
    )

    main_content = html.Div([
        dcc.Input(type='password',
                  placeholder="기존 비밀번호를 입력하세요",
                  id='more-password-input-old-password',
                  ),
    ], className="more-password-main-content-bar")
    return middle_content, main_content


def more_password_step_2_content():
    middle_content = dbc.Row(
        html.P(["비밀번호를 입력해주시길", html.Br(), "바랍니다."],
               className='more-password-text-content-value'),
    )

    main_content = html.Div([
        html.Div(
            [
                html.Label("비밀번호 입력",
                           className='more-password-password-label mt-3', ),
                html.Div([
                    dcc.Input(type='password',
                              placeholder="비밀번호를 입력하세요",
                              id='more-password-input-password',
                              style={'width': '80%'}
                              ),
                    html.I(className='ic-x w-20',
                           id='password-check-icon',
                           style={'font-size': '1.5rem', 'width': '1.5rem', 'height': '1.5rem'},
                           ),
                ], className='d-flex justify-content-between align-items-center w-100'),

            ], className="more-password-main-content-bar flex-column w-100 mb-5",
        ),
        html.Div(
            [
                html.Label("비밀번호 확인", className='more-password-password-label mt-3'),
                html.Div([
                    dcc.Input(type='password',
                              placeholder="비밀번호를 다시 입력하세요",
                              id='more-password-input-password-check',
                              style={'width': '80%'}
                              ),
                    html.I(className='ic-x w-20',
                           id='password-check-icon-verify',
                           style={'font-size': '1.5rem', 'width': '1.5rem', 'height': '1.5rem'},
                           ),
                ], className='d-flex justify-content-between align-items-center w-100'),
            ], className="more-password-main-content-bar flex-column w-100",
        )
    ], style={
        'boder': 'none',
        'flex-direction': 'column',
        'justify-content': 'start',
        'width': '80%',
    })
    return middle_content, main_content

def more_password_final_content():
    main_content = html.Div([
        html.P("비밀번호 변경 완료!",
               style={'color': '#1400FF', 'font-size': '1.2rem',
                      'font-weight': 'bold', 'text-align': 'center',
                      'margin-top': '10vh', 'margin-bottom': '10px'
                      }),
        html.H3(["다시 로그인해주세요."],
                style={'color': '#000000', 'font-weight': 'bold',
                       'text-align': 'center'}, id='more-password-final-name'),
    ], className="d-flex flex-column align-items-center justify-content-center text-center my-5")
    return "", main_content


def more_password_error_content():
    main_content = html.Div([
        html.P("오류 발생!",
               style={'color': 'red', 'font-size': '1.2rem',
                      'font-weight': 'bold', 'text-align': 'center',
                      'margin-top': '10vh', 'margin-bottom': '10px'
                      }),
    ], className="d-flex flex-column align-items-center justify-content-center text-center my-5")
    return "", main_content
