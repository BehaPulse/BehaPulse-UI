from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output


def more_layout():
    layout = html.Div([

        dcc.Location(id='more', refresh=True),  # 페이지 이동을 위한 Location

        # 오버레이 배경
        html.Div(id='more-overlay-background', style={
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
        html.Div(id='more-overlay-container', children=[
            html.Div([
                html.Div(["정말로 로그아웃", html.Br(), "하시겠습니까?"],
                         style={'font-size': '20px', 'padding': '10px', 'cursor': 'pointer'}),
                html.Div([
                    html.Div([
                        html.Div("확인", style={'font-size': '18px', 'padding': '10px', 'cursor': 'pointer',
                                              'background': '#003CFF', 'width': '40%', 'border-radius': '8px',
                                              'color': '#fff'},
                                 id='more-confirm-button'),
                        html.Div("취소", style={'font-size': '18px', 'padding': '10px', 'cursor': 'pointer',
                                              'background': '#D5D5D5', 'width': '40%', 'border-radius': '8px',
                                              'color': '#fff'},
                                 id='more-cancel-button')
                    ], style={'display': 'flex', 'width': '90%', 'justify-content': 'space-around'}),
                ],
                    style={'display': 'flex', 'width': '100%', 'justify-content': 'center', 'margin-top': '20px'},
                    id='more-overlay-buttons'
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
            }, id='more-overlay-content')
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
                        html.Span("",
                                  style={'font-weight': 'bold', 'color': '#3F3F3F', 'font-size': '1.5rem',
                                         'justify-content': 'center', 'align-items': 'center',
                                         'display': 'flex'}, id='more-name'),
                        className="d-flex align-items-center justify-content-center",
                        width="auto"
                    ),

                ], className="align-items-center mt-4 mb-3 justify-content-center", )

            ],
                id='more-header-content',
                className="d-flex justify-content-start mx-3",
            ),
        ]),

        # 중앙 영역
        dbc.Container([
            html.Div(children=more_content(), id='main-content', className='d-flex h-100 w-100'),
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
                        html.I(className='ic-more-selected', id='main-more-button-icon',
                               style={'cursor': 'pointer', 'width': '5vh', 'height': '5vh'}),
                        html.Div("더보기", className='text-bottom-selected'),
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


def more_content():
    content = html.Div([

        dbc.Row(
            html.Div([
                ""
            ], style={'background': '#F4F4F4', 'border-radius': '7px', 'width': '100%', 'height': '7vh',
                      'font-size': '1.25rem'}, id='more-id',
                className="d-flex align-items-center p-3")
            , className="w-100"),
        html.Div([
            more_item("ic-sensors", "동작 민감도 설정"),
            more_item("ic-hub", "SmartThings 설정"),
            more_item("", ""),
            more_item("ic-privacy-tip", "개인정보 방침 조항"),
            more_item("ic-description", "이용약관"),
            more_item("ic-info", "앱 정보"),
            more_item("ic-live-help", "도움말"),
            more_item("", ""),
            more_item("ic-key", "비밀번호 변경"),
            more_item("ic-logout", "로그아웃"),

        ], className='w-100 mt-4')

    ], className="d-flex align-items-center flex-column mx-3 h-100 w-100 justify-content-center")

    return content


def more_item(icon_class, label):
    return html.Div(
        [
            # 왼쪽 아이콘
            html.Div([
                html.I(className=icon_class, style={'height': '5vh', 'width': '5vh'}),
            ], style={'display': 'flex',
                      'justify-content': 'center', 'align-items': 'center',
                      'border-radius': '10px', 'width': '5vh', 'height': '5vh',
                      'margin-right': '20px',
                      },
            ),
            # 중앙 라벨
            html.Div([
                html.Span(label, style={'font-size': '1.25rem'}),
            ], style={'display': 'inline-block'}),

        ], style={'display': 'flex', 'justify-content': 'start', 'align-items': 'center',
                  'padding': '5px 0px', 'width': '95%', 'cursor': 'pointer', 'border-bottom': '1px solid #F4F4F4',},

        id={'type': 'more-item', 'index': label},
        n_clicks=0
    )
