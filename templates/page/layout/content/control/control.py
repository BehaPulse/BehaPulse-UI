from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output


def control_layout():
    layout = html.Div([

        dcc.Location(id='control', refresh=True),  # 페이지 이동을 위한 Location

        # 오버레이 배경
        html.Div(id='overlay-background', style={
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
        html.Div(id='overlay-container', children=[
            html.Div(style={
                'background': '#fff',
                'border-radius': '30px',
                'drop-shadow': '0 4px 4px rgba(0, 0, 0, 0.25)',
                'width': '40vh',
                'margin': 'auto',
                'padding': '20px',
                'position': 'relative',
                'textAlign': 'center'
            }, id='overlay-content')
        ], style={
            'display': 'none',
            'position': 'fixed',
            'top': '50%',
            'left': '50%',
            'transform': 'translate(-50%, -50%)',
            'zIndex': 2
        }),

        # 상단 영역
        dbc.Container([
            # 상단 영역
            html.Div([
                dbc.Row([
                    dbc.Col(
                        html.Span("",
                                  style={'font-weight': 'bold', 'color': '#3F3F3F', 'font-size': '1.5rem',
                                         'justify-content': 'center', 'align-items': 'center',
                                         'display': 'flex'}, id='main-location'),
                        className="d-flex align-items-center justify-content-center",
                        style={'padding-right': '0.25rem'},
                        width="auto",
                    ),
                    dbc.Col(
                        html.I(className='ic-arrow-down', id='main-down-button',
                               style={'font-size': '1.2rem', 'width': '1.5rem', 'height': '1.5rem',
                                      'cursor': 'pointer'},
                               ),
                        className="d-flex align-items-center justify-content-center",
                        style={'padding-left': '0.25rem'},
                        width="auto",
                    ),

                ], className="align-items-center mt-4 mb-3 justify-content-center", )

            ],
                className="d-flex justify-content-start mx-3",
            ),
        ]),

        # 중앙 영역
        dbc.Container([
            html.Div(children=control_content(), id='main-content', className='d-flex h-100 w-100'),
        ], className='flex-grow-1'),

        # 하단 영역
        dbc.Container([
            html.Div(
                [
                    html.Div([
                        html.I(className='ic-home', id='main-home-button-icon',
                               style={'cursor': 'pointer', 'width': '5vh', 'height': '5vh'}),
                        html.Div("홈", className='text-bottom'),
                    ], className='justify-content-center align-items-center d-flex flex-column text-center',
                        id='main-home-button'),
                    html.Div([
                        html.I(className='ic-desktop', id='main-device-button-icon',
                               style={'cursor': 'pointer', 'width': '5vh', 'height': '5vh'}),
                        html.Div("장치", className='text-bottom'),
                    ], className='justify-content-center align-items-center d-flex flex-column text-center',
                        id='main-device-button'),
                    html.Div([
                        html.I(className='ic-incandescent-selected', id='main-control-button-icon',
                               style={'cursor': 'pointer', 'width': '5vh', 'height': '5vh'}),
                        html.Div("조명", className='text-bottom-selected'),
                    ], className='justify-content-center align-items-center d-flex flex-column text-center',
                        id='main-control-button'),
                    html.Div([
                        html.I(className='ic-health-metrics', id='main-dashboard-button-icon',
                               style={'cursor': 'pointer', 'width': '5vh', 'height': '5vh'}),
                        html.Div("대시보드", className='text-bottom'),
                    ], className='justify-content-center align-items-center d-flex flex-column text-center',
                        id='main-dashboard-button'),
                    html.Div([
                        html.I(className='ic-more', id='main-more-button-icon',
                               style={'cursor': 'pointer', 'width': '5vh', 'height': '5vh'}),
                        html.Div("더보기", className='text-bottom'),
                    ], className='justify-content-center align-items-center d-flex flex-column text-center',
                        id='main-more-button'),
                ],
                className='d-flex justify-content-around align-items-center w-100',
            ),
        ],
            className='w-100 d-flex justify-content-end align-items-center mb-1',
            style={'height': '10vh', 'border-top': '1px solid rgba(0, 0, 0, 0.1)'}),
    ], className="min-vh-100 d-flex flex-column bg-white")

    return layout


def control_item(personId, name, gender, birth):
    """장치 항목 컴포넌트"""
    return html.Div([
        # 왼쪽 유저 정보
        html.Div([
            html.Div(name, style={'font-weight': 'bold', 'font-size': '20px'}),
            html.Div(
                [
                    html.Span(gender, style={'color': 'grey', 'font-size': '14px', 'margin-right': '10px'}),
                    html.Span(birth, style={'color': 'grey', 'font-size': '14px'}),
                ],
            ),
        ], style={'display': 'inline-block'}),

        # 오른쪽 텍스트 출력
        html.Div([
            html.Span(className='ic-chevron-right')
        ], style={'display': 'inline-block'}),

    ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center',
              'padding': '10px 0px', 'border-bottom': '1px solid #F4F4F4',
              'width': '100%'},

        # 행 전체가 클릭되도록 설정 (n_clicks 속성 추가)
        id={'type': 'control-row', 'index': personId},  # 각 줄에 고유 id 부여
        n_clicks=0,  # 클릭 수 초기화
    )


def control_content():
    content = html.Div([
        dbc.Row([
            # 제목
            html.Span("사용자 정보", style={'font-size': '1.25rem', 'font-weight': 'bold', 'padding': '0px'}),

            dcc.Loading(
                id="loading-spinner",
                type="circle",  # 다른 스피너 유형을 원할 경우 변경 가능
                children=html.Div(id='control-rows', className='w-100 mb-3',
                                  style={'height': '65vh', 'overflow-y': 'auto'}, ),
            ),

        ], className='w-100'),
    ], className="d-flex align-items-center flex-column mx-3 h-100 w-100 justify-content-center")

    return content



