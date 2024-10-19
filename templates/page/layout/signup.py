from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


# Define the layout
def signup_layout():
    layout = html.Div([
        dcc.Store(id='signup-data-store', data={}),  # 데이터를 저장할 숨겨진 Store
        dcc.Store(id='current-step-store', data=1),  # 현재 단계를 추적할 Store
        html.Div(id='dummy-output', style={'display': 'none'}),  # Dummy Output 추가
        dcc.Location(id='signup', refresh=True),  # 페이지 이동을 위한 Location
        dbc.Container([
            # 상단 영역: 뒤로가기 아이콘과 타이틀
            html.Div([
                dbc.Row([
                    dbc.Col(
                        html.I(className='ic-arrow-back', id='signup-back-button',
                               style={'font-size': '1.2rem', 'width': '1.5rem', 'height': '1.5rem',
                                      'cursor': 'pointer'},
                               ),
                        className="d-flex align-items-center justify-content-center",
                        width="auto",
                    ),
                    dbc.Col(
                        html.Span("회원가입",
                                  style={'font-weight': 'bold', 'color': '#3F3F3F', 'font-size': '1.5rem',
                                         'justify-content': 'center', 'align-items': 'center',
                                         'display': 'flex'}),
                        className="d-flex align-items-center justify-content-center",
                        width="auto"
                    ),
                ], className="align-items-center my-5 justify-content-center", )

            ],
                id='signup-header-content',
                className="d-flex justify-content-start mx-3",
            ),
            # 중간 영역: 설명 텍스트
            html.Div([

            ],
                className="d-flex flex-column justify-content-center mx-5 mt-5",
                id='signup-text-content'
            ),

            # 하단 영역: 입력 필드
            html.Div([
            ],
                className="d-flex flex-column justify-content-center align-items-center my-2",
                id='signup-main-content'
            )
        ], className="d-flex flex-column w-100 flex-grow-1"),  # flex-grow-1을 사용해 상단과 중간 영역을 확장 가능하게 설정

        dbc.Container([
            dbc.Row(
                dbc.Button("다음 단계",
                           id='signup-next-button',
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


def get_step_content(step):
    if step == 1:
        return sign_step_1_content()
    elif step == 2:
        return sign_step_2_content()
    elif step == 3:
        return sign_step_3_content()
    elif step == 4:
        return sign_step_4_content()
    elif step == 5:
        return sign_step_5_content()
    elif step == 6:
        return sign_step_6_content()
    elif step == 7:
        return sign_final_content()
    elif step == 8:
        return sign_error_content()
    else:
        return "Unknown Step", ""


def sign_step_1_content():
    middle_content = dbc.Row(
        html.P(["BehaPulse와 함께할 이름을", html.Br(), "적어주시길 바랍니다"],
               className='sign-text-content-value'),
    )

    main_content = html.Div([
        dcc.Input(type='text',
                  placeholder="이름을 입력하세요",
                  id='sign-input-name'
                  ),
    ], className="sign-main-content-bar")
    return middle_content, main_content


def sign_step_2_content():
    middle_content = dbc.Row(
        html.P(["와이파이 센싱으로 편안하고", html.Br(), "안전한 케어를 제공합니다"],
               className='sign-text-content-value'),
    )

    main_content = html.Div(
        [
            html.Div("성별",
                     style={
                         'font-size': '1.2rem',
                         'text-align': 'center',
                         'width': '26%',
                         'padding': '1px 2px',
                     }),

            dbc.Button("남성", className='sign-input-gender', id='sign-input-gender-man'),
            dbc.Button("여성", className='sign-input-gender', id='sign-input-gender-woman'),
        ],
        className='sign-main-content-bar'
    )
    return middle_content, main_content


def sign_step_3_content():
    # 중간 영역: 설명 텍스트
    middle_content = dbc.Row(
        html.P(["생년월일을 입력해주시길", html.Br(), "바랍니다."],
               className='sign-text-content-value'),
    )

    # 날짜 입력 필드를 포함한 전체 컨테이너와 하나의 밑줄
    main_content = html.Div(
        [
            # 연도 입력 필드
            dcc.Input(
                type='number', placeholder="YYYY", max=9999, min=1000,
                className='sign-input-date',
                style={
                    'outline': 'none',
                    'box-shadow': 'none',
                },
                id='sign-input-year'
            ),
            # 월 입력 필드
            dcc.Input(
                type='number', placeholder="MM", max=12, min=1,
                className='sign-input-date',
                style={
                    'outline': 'none',
                    'box-shadow': 'none',
                },
                id='sign-input-month'
            ),
            # 일 입력 필드
            dcc.Input(
                type='number', placeholder="DD", max=31, min=1,
                className='sign-input-date',
                style={
                    'outline': 'none',
                    'box-shadow': 'none',
                },
                id='sign-input-day'
            )
        ],
        className='sign-main-content-bar'
    )
    return middle_content, main_content


def sign_step_4_content():
    middle_content = dbc.Row(
        html.P([" 아이디를 입력해주시길", html.Br(), "바랍니다."],
               className='sign-text-content-value'),
    )

    main_content = html.Div([
        dcc.Input(type='text',
                  placeholder="아이디를 입력하세요",
                  id='sign-input-id'
                  ),
        dbc.Button("중복확인", id='sign-duplicate-check-btn'),
    ], className="sign-main-content-bar"
    )
    return middle_content, main_content


def sign_step_5_content():
    middle_content = dbc.Row(
        html.P(["비밀번호를 입력해주시길", html.Br(), "바랍니다."],
               className='sign-text-content-value'),
    )

    main_content = html.Div([
        html.Div(
            [
                html.Label("비밀번호 입력",
                           className='sign-password-label mt-3', ),
                html.Div([
                    dcc.Input(type='password',
                              placeholder="비밀번호를 입력하세요",
                              id='sign-input-password',
                              style={'width': '80%'}
                              ),
                    html.I(className='ic-x w-20',
                           id='password-check-icon',
                           style={'font-size': '1.5rem', 'width': '1.5rem', 'height': '1.5rem'},
                           ),
                ], className='d-flex justify-content-between align-items-center w-100'),

            ], className="sign-main-content-bar flex-column w-100 mb-5",
        ),
        html.Div(
            [
                html.Label("비밀번호 확인", className='sign-password-label mt-3'),
                html.Div([
                    dcc.Input(type='password',
                              placeholder="비밀번호를 다시 입력하세요",
                              id='sign-input-password-check',
                              style={'width': '80%'}
                              ),
                    html.I(className='ic-x w-20',
                           id='password-check-icon-verify',
                           style={'font-size': '1.5rem', 'width': '1.5rem', 'height': '1.5rem'},
                           ),
                ], className='d-flex justify-content-between align-items-center w-100'),
            ], className="sign-main-content-bar flex-column w-100",
        )
    ], style={
        'boder': 'none',
        'flex-direction': 'column',
        'justify-content': 'start',
        'width': '80%',
    })
    return middle_content, main_content


def sign_step_6_content():
    middle_content = dbc.Row(
        html.P(["비밀번호 찾기를 위한", html.Br(), "보안 질문을 설정해 주세요."],
               className='sign-text-content-value'),
    )

    main_content = html.Div([
        html.Div(
            [
                html.Label("보안 질문 입력",
                           className='sign-password-label mt-3'),
                html.Div([
                    dcc.Input(type='text',
                              placeholder="보안 질문을 입력하세요",
                              id='sign-input-security-question',
                              style={'width': '80%'}
                              ),
                ], className='d-flex justify-content-between align-items-center w-100'),

            ], className="sign-main-content-bar flex-column w-100 mb-5",
        ),
        html.Div(
            [
                html.Label("답변 입력", className='sign-password-label mt-3'),
                html.Div([
                    dcc.Input(type='text',
                              placeholder="답변을 입력하세요",
                              id='sign-input-security-answer',
                              style={'width': '80%'}
                              ),
                ], className='d-flex justify-content-between align-items-center w-100'),
            ], className="sign-main-content-bar flex-column w-100",
        )
    ], style={
        'boder': 'none',
        'flex-direction': 'column',
        'justify-content': 'start',
        'width': '80%',
    })

    return middle_content, main_content


def sign_final_content():
    main_content = html.Div([
        html.P("가입 완료!",
               style={'color': '#1400FF', 'font-size': '1.2rem',
                      'font-weight': 'bold', 'text-align': 'center',
                      'margin-top': '10vh', 'margin-bottom': '10px'
                      }),
        html.H3(f"홍길동님, 환영해요",
                style={'color': '#000000', 'font-weight': 'bold',
                       'text-align': 'center'}, id='signup-final-name'),
    ], className="d-flex flex-column align-items-center justify-content-center text-center my-5")
    return "", main_content


def sign_error_content():
    main_content = html.Div([
        html.P("오류 발생!",
               style={'color': 'red', 'font-size': '1.2rem',
                      'font-weight': 'bold', 'text-align': 'center',
                      'margin-top': '10vh', 'margin-bottom': '10px'
                      }),
    ], className="d-flex flex-column align-items-center justify-content-center text-center my-5")
    return "", main_content
