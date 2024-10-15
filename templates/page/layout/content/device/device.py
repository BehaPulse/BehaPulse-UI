from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output

from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output

# 색상 정의
status_colors = {
    "active": "#00D84F",  # 녹색
    "inactive": "#E10000"  # 빨간색
}


def device_layout():
    layout = html.Div([

        dcc.Location(id='device', refresh=True),  # 페이지 이동을 위한 Location

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
            html.Div([
                html.Div("길병원", style={'font-size': '18px', 'padding': '10px', 'cursor': 'pointer'}, id='gil-button'),
                html.Div("아산병원", style={'font-size': '18px', 'padding': '10px', 'cursor': 'pointer'}, id='asan-button'),
                html.Div("중앙병원", style={'font-size': '18px', 'padding': '10px', 'cursor': 'pointer'},
                         id='jungang-button')
            ], style={
                'background': '#fff',
                'border-radius': '30px',
                'drop-shadow': '0 4px 4px rgba(0, 0, 0, 0.25)',
                'width': '40vh',
                'margin': 'auto',
                'padding': '20px',
                'position': 'relative',
                'textAlign': 'center'
            })
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
                        html.Span("미사1동",
                                  style={'font-weight': 'bold', 'color': '#3F3F3F', 'font-size': '1.5rem',
                                         'justify-content': 'center', 'align-items': 'center',
                                         'display': 'flex'}),
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

                ], className="align-items-center mt-5 mb-3 justify-content-center", )

            ],
                className="d-flex justify-content-start mx-3",
            ),
        ]),

        # 중앙 영역
        dbc.Container([
            html.Div(children=device_content(), id='main-content', className='d-flex h-100 w-100'),
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
                        html.I(className='ic-desktop-selected', id='main-device-button-icon',
                               style={'cursor': 'pointer', 'width': '5vh', 'height': '5vh'}),
                        html.Div("장치", className='text-bottom-selected'),
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

# 재사용 가능한 장치 항목 컴포넌트 함수
def device_item(name, mac_address, status):
    """장치 항목 컴포넌트"""
    return html.Div(
        [
            # 왼쪽 장치 정보
            html.Div([
                html.Div(name, style={'font-weight': 'bold', 'font-size': '20px'}),
                html.Div(mac_address, style={'color': 'grey', 'font-size': '14px'}),
            ], style={'display': 'inline-block'}),

            # 오른쪽 상태 아이콘
            html.Div([
                html.Span(style={
                    'backgroundColor': status_colors[status],
                    'width': '2.5vh',
                    'height': '2.5vh',
                    'border-radius': '6px',
                    'display': 'inline-block'
                })
            ], style={'display': 'inline-block'}),

        ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center',
                  'padding': '10px 0px', 'border-bottom': '1px solid #F4F4F4',
                  'width': '100%'},

        # 행 전체가 클릭되도록 설정 (n_clicks 속성 추가)
        id={'type': 'device-row', 'index': mac_address},  # 각 줄에 고유 id 부여
        n_clicks=0,  # 클릭 수 초기화
    )


def device_content():
    content = html.Div([
        dcc.Store(id='device-data-store', data={}),  # 데이터를 저장할 숨겨진 Store
        dbc.Row([
            # 제목
            html.Span("장치 정보", style={'font-size': '1.25rem', 'font-weight': 'bold', 'padding': '0px'}),

            dcc.Loading(
                id="loading-spinner",
                type="circle",  # 다른 스피너 유형을 원할 경우 변경 가능
                children=html.Div(id='device-rows', className='w-100 mb-3',
                                  style={'height': '65vh', 'overflow-y': 'auto'},),
            ),

            html.Div([
                dbc.Button([
                    # 아이콘과 텍스트를 버튼 안에 배치
                    html.I(className='ic-device-add me-1', style={'width': '2rem', 'height': '2rem'}),
                    html.Span("장치 추가", style={'font-size': '1rem', 'font-weight': 'bold'})
                ], color="primary", id='device-add-button', href='/beha-pulse/main/device/add/'),
            ], className='d-flex justify-content-end w-100 p-0')
        ], className='w-100'),

    ], className="d-flex align-items-center flex-column mx-3 h-100 w-100 justify-content-center")

    return content
