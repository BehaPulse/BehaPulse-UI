from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output


def main_layout():
    layout = html.Div([
        dcc.Location(id='main', refresh=False),  # 페이지 이동을 위한 Location

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
            # 'top': '10vh',
            # 'left': '5vw',
            # 'transform': 'translate(-10vw, -10vh)',
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
            dcc.Loading(
                id="loading-spinner",
                type="circle",  # 다른 스피너 유형을 원할 경우 변경 가능
                children=html.Div(main_content(), id='main-content', className='d-flex h-100 w-100'),
            ),

        ], className='flex-grow-1', style={'padding': '0px 3vh'}),

        # 하단 영역
        dbc.Container([
            html.Div(
                [
                    html.Div([
                        html.I(className='ic-home-selected', id='main-home-button-icon',
                               style={'cursor': 'pointer', 'width': '5vh', 'height': '5vh'}),
                        html.Div("홈", className='text-bottom-selected'),
                    ], className='justify-content-center align-items-center d-flex flex-column text-center',
                        id='main-home-button'),
                    html.Div([
                        html.I(className='ic-desktop', id='main-device-button-icon',
                               style={'cursor': 'pointer', 'width': '5vh', 'height': '5vh'}),
                        html.Div("장치", className='text-bottom'),
                    ], className='justify-content-center align-items-center d-flex flex-column text-center',
                        id='main-device-button'),
                    html.Div([
                        html.I(className='ic-incandescent', id='main-control-button-icon',
                               style={'cursor': 'pointer', 'width': '5vh', 'height': '5vh'}),
                        html.Div("조명", className='text-bottom'),
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


def main_content():
    content = html.Div([

        dbc.Row([
            html.Div([
                html.Img(
                         # object-fit 추후 수정 필요
                         style={'width': '100%', 'height': '100%', 'objectFit': 'contain'}, id='profile-image'),
            ], className='main-profile-circle')
        ], className='d-flex justify-content-center align-items-center mb-3'),

        dbc.Row([
            html.Div([
                html.Span("", style={'font-size': '1.5rem', 'font-weight': 'bold'}, id='main-user-name'),
            ], className='d-flex justify-content-center align-items-center mb-3'),
        ], ),

        # Content Boxes
        dbc.Row(
            dbc.Card([
                dbc.CardBody([
                    html.Div("관리하는 장치의 수",
                             style={'font-size': '1.3rem', 'font-weight': 'bold', 'margin': '10px 0px'}),
                    html.Div("현재 개의 장치를 관리하고 있습니다.",
                             style={'font-size': '1.1rem', 'color': '#A9A9A9', 'margin': '3vh 0px'},
                             id='main-device-count'),
                ]),
            ], className='main-card-body'),
            className="main-card-container w-100 mx-3 my-2",
        ),
        # Content Boxes
        dbc.Row(
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.Div(html.I(className='ic-sensors', style={'width': '10vh', 'height': '10vh'}),
                                 style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),
                        html.Div(style={'flex': '1'}),
                        html.Div([
                            html.Div("민감도 설정",
                                     style={'font-size': '1.3rem', 'font-weight': 'bold', 'margin-top': '10px',
                                            'justify-content': 'flex-end', 'display': 'flex'}),
                            html.Div("동작별 민감도 설정",
                                     style={'font-size': '1.1rem', 'color': '#A9A9A9', 'margin': '3vh 0px'}),
                        ]),
                    ], id='main-sensitivity-button', n_clicks=0, style={'display': 'flex', 'width': '100%'}, ),
                ], style={'display': 'flex', 'flex-direction': 'row'}, ),
            ], className='main-card-body'),
            className="main-card-container w-100 mx-3 my-2",
        ),
        # Content Boxes

    ], className="d-flex justify-content-center align-items-center flex-column w-100 h-100",
    )
    return content
