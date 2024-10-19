from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output


def control_setting_layout():
    layout = html.Div([
        dbc.Container([
            # 상단 영역: 뒤로가기 아이콘과 타이틀
            html.Div([
                dbc.Row([
                    dbc.Col(
                        html.I(className='ic-arrow-back', id='control-back-button',
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
                ], className="align-items-center mt-5 mb-5 justify-content-center", )

            ],
                className="d-flex justify-content-start mx-3",
            ),
        ]),

        dbc.Container([
            dcc.Loading(
                id="loading-spinner",
                type="circle",
                children=html.Div(children=control_setting_content(), id='main-content', className='d-flex w-100')
            )
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


def control_setting_content():
    content = html.Div([
        dbc.Row([
            html.Div([
                html.Div(html.Img(src='../../../assets/img/Lying_down.svg', style={'height': '7vh', 'width': '7vh'}),
                         style={'display': 'flex', 'background-color': '#EEEEEE',
                                'justify-content': 'center', 'align-items': 'center',
                                'border-radius': '10px', 'width': '10vh', 'height': '10vh',
                                },
                         id='control-lying-down', n_clicks=0),
                html.Div(html.Img(src='../../../assets/img/empty.svg', style={'height': '7vh', 'width': '7vh'}),
                         style={'display': 'flex', 'background-color': '#EEEEEE',
                                'justify-content': 'center', 'align-items': 'center',
                                'border-radius': '10px', 'width': '10vh', 'height': '10vh',
                                },
                         id='control-empty-down', n_clicks=0),
                html.Div(html.Img(src='../../../assets/img/Sitting_down.svg', style={'height': '7vh', 'width': '7vh'}),
                         style={'display': 'flex', 'background-color': '#EEEEEE',
                                'justify-content': 'center', 'align-items': 'center',
                                'border-radius': '10px', 'width': '10vh', 'height': '10vh',
                                },
                         id='control-sitting-down', n_clicks=0),

            ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center', 'width': '100%'}),
        ], className="w-100 p-0"),

        dbc.Row([
            html.Div(style={
                'width': '25vh',  # 원의 크기
                'height': '25vh',
                'border-radius': '50%',  # 원 모양
                'background-color': '#18E8FF',
                'box-shadow': '0px 0px 50px 20px #18E8FF',  # 부드러운 그림자 효과
                'margin': 'auto',
                'position': 'relative'  # 다른 요소를 이 위에 배치하기 위한 설정
            }, id='contorl_setting_circle'),
        ], className="w-100 p-0", style={'margin-top': '15vh'}),

        dbc.Row([
            html.Div(
                [
                    html.I(style={'width': '4vh', 'height': '4vh'}),
                    html.I(style={'width': '4vh', 'height': '4vh',
                                  'display': 'inline-block', 'background-repeat': 'no-repeat',
                                  'background-size': '100% 100%;',
                                  'background-image': 'url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 24 24\'%3E%3Cpath fill=\'%23B7B7B7\' d=\'m15.3 16.7l1.4-1.4l-3.7-3.7V7h-2v5.4zM12 22q-2.075 0-3.9-.788t-3.175-2.137T2.788 15.9T2 12t.788-3.9t2.137-3.175T8.1 2.788T12 2t3.9.788t3.175 2.137T21.213 8.1T22 12t-.788 3.9t-2.137 3.175t-3.175 2.138T12 22m0-2q3.325 0 5.663-2.337T20 12t-2.337-5.663T12 4T6.337 6.338T4 12t2.338 5.663T12 20\'/%3E%3C/svg%3E")',
                                  }, id='ic-schedule'),
                    html.Span("", style={'font-size': '1.25rem', "font-weight": 'bold'},
                              id='control-setting-now-status'),
                    html.I(style={'width': '4vh', 'height': '4vh'}),
                ]
                , style={'background': '#FFFFFF', 'box-shadow': '0px 0px 17px 2px rgba(0, 0, 0, 0.13)',
                         'border-radius': '15px', 'width': '80%', 'height': '7vh', 'display': 'flex',
                         'align-items': 'center', 'justify-content': 'space-between'}
            )
        ], className="w-100 p-0", style={'margin-top': '10vh', 'display': 'flex', 'justify-content': 'center'}),

    ], className="d-flex align-items-center flex-column mx-3 w-100")
    return content
