import os

from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


def more_info_layout():
    layout = html.Div([

        dbc.Container([
            # 상단 영역: 뒤로가기 아이콘과 타이틀
            html.Div([
                dbc.Row([
                    dbc.Col(
                        html.I(className='ic-arrow-back', id='more-back-button',
                               style={'font-size': '1.2rem', 'width': '1.5rem', 'height': '1.5rem',
                                      'cursor': 'pointer'},
                               ),
                        className="d-flex align-items-center justify-content-center",
                        width="auto",
                    ),
                    dbc.Col(
                        html.Span("앱정보",
                                  style={'font-weight': 'bold', 'color': '#3F3F3F', 'font-size': '1.5rem',
                                         'justify-content': 'center', 'align-items': 'center',
                                         'display': 'flex'}),
                        className="d-flex align-items-center justify-content-center",
                        width="auto"
                    ),
                ], className="align-items-center mt-4 mb-3 justify-content-center", )

            ],
                className="d-flex justify-content-start mx-3",
            ),
        ]),

        dbc.Container([
            html.Div(children=more_info_content(), id='main-content', className='d-flex w-100',
                     style={'height': '75vh', 'overflow-y': 'auto'}),
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


def more_info_content():
    content = html.Div([
        dbc.Row([
            html.Span("버전정보", style={'font-size': '1rem', 'padding': '0px', 'color': '#3F3F3F'}),
            html.Div([
                html.Div([
                    html.Img(src="../../../assets/img/logo.svg", style={'height': '6vh', 'width': '6vh'}),
                ], style={'display': 'flex', 'background-color': '#003CFF',
                          'justify-content': 'center', 'align-items': 'center',
                          'border-radius': '10px', 'width': '7vh', 'height': '7vh',
                          'margin-right': '20px'
                          },
                ),
                html.Div([
                    html.Div("Behapulse", style={'font-size': '1rem'}),
                    html.Div("1.2.1", style={'color': '#848484', 'font-size': '0.75rem'}),
                ], style={'display': 'inline-block'}),
            ], style={'display': 'flex', 'align-items': 'center', 'margin-top': '20px'}),
        ], className="w-100 p-0"),
        html.Hr(style={'border-top': '1px solid #3F4F4F', 'width': '100%', 'margin': '20px 0px'}),
        dbc.Row([
            html.Span("제작자", style={'font-size': '1rem', 'padding': '0px', 'color': '#3F3F3F'}),
            html.Div([
                html.Div([
                    html.Img(src="../../../assets/img/symbolmark.jpg", style={'height': '6vh', 'width': '6vh'}),
                ], style={'display': 'flex', 'border': '2px solid #848484',
                          'justify-content': 'center', 'align-items': 'center',
                          'border-radius': '10px', 'width': '7vh', 'height': '7vh',
                          'margin-right': '20px'
                          },
                ),
                html.Div([
                    html.Div("INC LAB", style={'font-size': '1rem'}),
                    html.Div("since 2015", style={'color': '#848484', 'font-size': '0.75rem'}),
                ], style={'display': 'inline-block'}),
            ], style={'display': 'flex', 'align-items': 'center', 'margin-top': '20px'}),
        ], className="w-100 p-0")

    ], className="d-flex align-items-center flex-column mx-3 w-100")
    return content
