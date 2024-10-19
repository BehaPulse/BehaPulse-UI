import os

from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

def main_sensitivity_layout():
    layout = html.Div([

        dbc.Container([
            # 상단 영역: 뒤로가기 아이콘과 타이틀
            html.Div([
                dbc.Row([
                    dbc.Col(
                        html.I(className='ic-arrow-back', id='main-back-button',
                               style={'font-size': '1.2rem', 'width': '1.5rem', 'height': '1.5rem',
                                      'cursor': 'pointer'},
                               ),
                        className="d-flex align-items-center justify-content-center",
                        width="auto",
                    ),
                    dbc.Col(
                        html.Span("민감도 설정",
                                  style={'font-weight': 'bold', 'color': '#3F3F3F', 'font-size': '1.5rem',
                                         'justify-content': 'center', 'align-items': 'center',
                                         'display': 'flex'}),
                        className="d-flex align-items-center justify-content-center",
                        width="auto"
                    ),
                ], className="align-items-center mt-5 mb-4 justify-content-center", )

            ],
                className="d-flex justify-content-start mx-3",
            ),
        ]),
        
        dbc.Container([
            dcc.Loading(
                id="loading-spinner",
                type="circle",
                children=html.Div(children=main_sensitivity_content(), 
                                  id='main-content', 
                                  className='d-flex w-100',
                                    style={'height': '75vh', 'overflow-y': 'auto'})
            )
        ], className='flex-grow-1'),

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

def main_sensitivity_content():
    content = html.Div([
        
        dbc.Row([
            # 왼쪽 아이콘
            html.Div(html.Img(src='../../assets/img/Lying_down.svg', style={'height': '5vh', 'width': '5vh'}),
                         style={'display': 'flex', 'background-color': '#EEEEEE',
                                'justify-content': 'center', 'align-items': 'center',
                                'border-radius': '10px', 'width': '7vh', 'height': '7vh',
                                },),
            html.Div(['누워있음'], 
                     style={'display': 'flex', 
                            'align-items': 'center', 
                            'width': '50%', 
                            'padding-left':'20px',
                            'font-size': '1.25rem', 
                            'font-weight': 'bold'}),
        # Slider
        html.Div([
            html.Div([
                html.Span(className='ic-sensors-krx-outline', style={'margin-right': '10px', 'width': '5vh', 'height': '5vh'}),

                dcc.Slider(id='main-sensitivity-lying-slider',
                           min=0.5,
                           max=1.5,
                           value=1,
                           marks={0.5: '', 1.5: ''},  # 빈 공간으로 양쪽 마크
                           step=0.1,
                           tooltip={'placement': 'bottom', 'always_visible': False},
                           updatemode='drag',  # 슬라이더를 드래그할 때 업데이트
                           className="flex-grow-1 p-0",
                           ),  # 슬라이더가 영역을 차지하게 함),
                html.Span(className='ic-sensors-krx', style={'margin-left': '10px', 'width': '5vh', 'height': '5vh'}),

            ], style={'background': '#EEEEEE', 'border-radius': '25px', 'transform: ': 'matrix(-1, 0, 0, 1, 0, 0)',
                      'justify-content': 'space-between',
                      'width': '100%', 'height': '7vh', 'display': 'flex', 'align-items': 'center',
                      'padding': '0 20px'}),
        ], style={'margin': '20px 0px', 'width': '100%', 'padding' : '0px'}),
            
        ], className="w-100 p-0 d-flex"),
        
        dbc.Row([
            # 왼쪽 아이콘
            html.Div(html.Img(src='../../assets/img/empty.svg', style={'height': '5vh', 'width': '5vh'}),
                         style={'display': 'flex', 'background-color': '#EEEEEE',
                                'justify-content': 'center', 'align-items': 'center',
                                'border-radius': '10px', 'width': '7vh', 'height': '7vh',
                                },),
            html.Div(['비어있음'], 
                     style={'display': 'flex', 
                            'align-items': 'center', 
                            'width': '50%', 
                            'padding-left':'20px',
                            'font-size': '1.25rem', 
                            'font-weight': 'bold'}),
        # Slider
        html.Div([
            html.Div([
                html.Span(className='ic-sensors-krx-outline', style={'margin-right': '10px', 'width': '5vh', 'height': '5vh'}),

                dcc.Slider(id='main-sensitivity-empty-slider',
                           min=0.5,
                           max=1.5,
                           value=1,
                           marks={0.5: '', 1.5: ''},  # 빈 공간으로 양쪽 마크
                           step=0.1,
                           tooltip={'placement': 'bottom', 'always_visible': False},
                           updatemode='drag',  # 슬라이더를 드래그할 때 업데이트
                           className="flex-grow-1 p-0",
                           ),  # 슬라이더가 영역을 차지하게 함),
                html.Span(className='ic-sensors-krx', style={'margin-left': '10px', 'width': '5vh', 'height': '5vh'}),

            ], style={'background': '#EEEEEE', 'border-radius': '25px', 'transform: ': 'matrix(-1, 0, 0, 1, 0, 0)',
                      'justify-content': 'space-between',
                      'width': '100%', 'height': '7vh', 'display': 'flex', 'align-items': 'center',
                      'padding': '0 20px'}),
        ], style={'margin': '20px 0px', 'width': '100%', 'padding' : '0px'}),
            
        ], className="w-100 p-0 d-flex"),
        
        dbc.Row([
            # 왼쪽 아이콘
            html.Div(html.Img(src='../../assets/img/Sitting_down.svg', style={'height': '5vh', 'width': 'vh'}),
                         style={'display': 'flex', 'background-color': '#EEEEEE',
                                'justify-content': 'center', 'align-items': 'center',
                                'border-radius': '10px', 'width': '7vh', 'height': '7vh',
                                },),
            html.Div(['앉아있음'], 
                     style={'display': 'flex', 
                            'align-items': 'center', 
                            'width': '50%', 
                            'padding-left':'20px',
                            'font-size': '1.25rem', 
                            'font-weight': 'bold'}),
        # Slider
        html.Div([
            html.Div([
                html.Span(className='ic-sensors-krx-outline', style={'margin-right': '10px', 'width': '5vh', 'height': '5vh'}),

                dcc.Slider(id='main-sensitivity-sitting-slider',
                           min=0.5,
                           max=1.5,
                           value=1,
                           marks={0.5: '', 1.5: ''},  # 빈 공간으로 양쪽 마크
                           step=0.1,
                           tooltip={'placement': 'bottom', 'always_visible': False},
                           updatemode='drag',  # 슬라이더를 드래그할 때 업데이트
                           className="flex-grow-1 p-0",
                           ),  # 슬라이더가 영역을 차지하게 함),
                html.Span(className='ic-sensors-krx', style={'margin-left': '10px', 'width': '5vh', 'height': '5vh'}),

            ], style={'background': '#EEEEEE', 'border-radius': '25px', 'transform: ': 'matrix(-1, 0, 0, 1, 0, 0)',
                      'justify-content': 'space-between',
                      'width': '100%', 'height': '7vh', 'display': 'flex', 'align-items': 'center',
                      'padding': '0 20px'}),
        ], style={'margin': '20px 0px', 'width': '100%', 'padding' : '0px'}),
            
        ], className="w-100 p-0 d-flex"),
        
        dbc.Row(
                dbc.Button("저장하기",
                           id='main-sensitivity-save-button',
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
            )
        
        
    ], className="d-flex align-items-center flex-column mx-3 w-100", style={'justify-content': 'space-between'})

    return content
    