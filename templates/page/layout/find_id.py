from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


# Define the layout
def find_id_layout():
    layout = html.Div([
        dcc.Store(id='find-id-data-store', data={}),  # 데이터를 저장할 숨겨진 Store
        dcc.Store(id='find-id-current-step-store', data=1),  # 현재 단계를 추적할 Store
        html.Div(id='dummy-output', style={'display': 'none'}),  # Dummy Output 추가
        dcc.Location(id='find-id', refresh=True),  # 페이지 이동을 위한 Location
        dbc.Container([
            # 상단 영역: 뒤로가기 아이콘과 타이틀
            html.Div([
                dbc.Row([
                    dbc.Col(
                        html.I(className='ic-arrow-back', id='find-id-back-button',
                               style={'font-size': '1.2rem', 'width': '1.5rem', 'height': '1.5rem',
                                      'cursor': 'pointer'},
                               ),
                        className="d-flex align-items-center justify-content-center",
                        width="auto",
                    ),
                    dbc.Col(
                        html.Span("아이디 찾기",
                                  style={'font-weight': 'bold', 'color': '#3F3F3F', 'font-size': '1.5rem',
                                         'justify-content': 'center', 'align-items': 'center',
                                         'display': 'flex'}),
                        className="d-flex align-items-center justify-content-center",
                        width="auto"
                    ),
                ], className="align-items-center my-5 justify-content-center", )

            ],
                id='find-id-header-content',
                className="d-flex justify-content-start mx-3",
            ),
            # 중간 영역: 설명 텍스트
            html.Div([

            ],
                className="d-flex flex-column justify-content-center mx-5 mt-5",
                id='find-id-text-content'
            ),

            # 하단 영역: 입력 필드
            html.Div([
            ],
                className="d-flex flex-column justify-content-center align-items-center my-2",
                id='find-id-main-content'
            )
        ], className="d-flex flex-column w-100 flex-grow-1"),  # flex-grow-1을 사용해 상단과 중간 영역을 확장 가능하게 설정

        dbc.Container([
            dbc.Row(
                dbc.Button("다음",
                           id='find-id-next-button',
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
        return find_id_step_1_content()
    elif step == 2:
        return find_id_step_2_content()
    elif step == 3:
        return find_id_final_content()
    elif step == 4:
        return find_id_error_content()
    elif step == 5:
        return find_id_no_content()
    else:
        return "Unknown Step", ""


def find_id_step_1_content():
    middle_content = dbc.Row(
        html.P(["이름을 입력해주세요"],
               className='find-id-text-content-value'),
    )

    main_content = html.Div([
        dcc.Input(type='text',
                  placeholder="",
                  id='find-id-input-name'
                  ),
    ], className="find-id-main-content-bar")
    return middle_content, main_content


def find_id_step_2_content():
    # 중간 영역: 설명 텍스트
    middle_content = dbc.Row(
        html.P(["생년월일을 입력해주시길 바랍니다."],
               className='find-id-text-content-value'),
    )

    # 날짜 입력 필드를 포함한 전체 컨테이너와 하나의 밑줄
    main_content = html.Div(
        [
            # 연도 입력 필드
            dcc.Input(
                type='number', placeholder="YYYY", max=9999, min=1000,
                className='find-id-input-date',
                style={
                    'outline': 'none',
                    'box-shadow': 'none',
                },
                id='find-id-input-year'
            ),
            # 월 입력 필드
            dcc.Input(
                type='number', placeholder="MM", max=12, min=1,
                className='find-id-input-date',
                style={
                    'outline': 'none',
                    'box-shadow': 'none',
                },
                id='find-id-input-month'
            ),
            # 일 입력 필드
            dcc.Input(
                type='number', placeholder="DD", max=31, min=1,
                className='find-id-input-date',
                style={
                    'outline': 'none',
                    'box-shadow': 'none',
                },
                id='find-id-input-day'
            )
        ],
        className='find-id-main-content-bar'
    )
    return middle_content, main_content


def find_id_final_content():
    main_content = html.Div([
        html.P("",
               style={'color': '#003CFF', 'font-size': '1.2rem',
                      'font-weight': 'bold', 'text-align': 'center',
                      'margin-top': '10vh', 'margin-bottom': '10px'
                      }, id='find-final-name'),
        html.H3(f"",
                style={'color': '#000000', 'font-weight': 'bold',
                       'text-align': 'center'}, id='find-final-id'),
    ], className="d-flex flex-column align-items-center justify-content-center text-center my-5")
    return "", main_content


def find_id_error_content():
    main_content = html.Div([
        html.P("오류 발생!",
               style={'color': 'red', 'font-size': '1.2rem',
                      'font-weight': 'bold', 'text-align': 'center',
                      'margin-top': '20vh', 'margin-bottom': '10px'
                      }),
    ], className="d-flex flex-column align-items-center justify-content-center text-center my-5")
    return "", main_content


def find_id_no_content():
    main_content = html.Div([
        html.P("가입된 ID가 없습니다.",
               style={'color': '#000000', 'font-size': '1.2rem',
                      'font-weight': 'bold', 'text-align': 'center',
                      'margin-top': '20vh', 'margin-bottom': '10px'
                      }),
    ], className="d-flex flex-column align-items-center justify-content-center text-center my-5")
    return "", main_content
