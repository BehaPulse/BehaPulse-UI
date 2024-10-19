import os

from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

import plotly.graph_objects as go

fig = go.Figure(data=px.line(x=[1, 2, 3], y=[1, 3, 2]))
fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    xaxis_title='',
    yaxis_title='',
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
)


def dashboard_detail_layout():
    layout = html.Div([

        dbc.Container([
            # 상단 영역: 뒤로가기 아이콘과 타이틀
            html.Div([
                dbc.Row([
                    dbc.Col(
                        html.I(className='ic-arrow-back', id='dashboard-detail-back-button',
                               style={'font-size': '1.2rem', 'width': '1.5rem', 'height': '1.5rem',
                                      'cursor': 'pointer'},
                               ),
                        className="d-flex align-items-center justify-content-center",
                        width="auto",
                    ),
                    dbc.Col(
                        html.Span("사용자 정보",
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
            dcc.Loading(
                id="loading-spinner",
                type="circle",
                children=html.Div(children=dashboard_detail_content(), id='main-content', className='d-flex w-100')
            )
        ], className='flex-grow-1'),

        dbc.Container(
            dbc.Row([
                html.Div(
                    [
                        dcc.Graph(id='live-graph',
                                  config={'displayModeBar': False},
                                  style={'height': '100%', 'width': '100%'},
                                  className='p-0'),
                        dcc.Interval(
                            id='graph-update',
                            interval=2000,  # Update graph every second
                            n_intervals=0
                        ), ]
                    , style={'width': '100%', 'height': '37vh', 'display': 'flex', })
            ], className='d-flex justify-content-between align-items-center w-100'),
            className='d-flex justify-content-center align-items-center w-100 mb-4'
        ),

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
                        html.I(className='ic-health-metrics-selected', id='main-dashboard-button-icon',
                               style={'cursor': 'pointer', 'width': '5vh', 'height': '5vh'}),
                        html.Div("대시보드", className='text-bottom-selected'),
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


def dashboard_detail_content():
    content = html.Div([
        dbc.Row([
            html.Div([
                html.Img(style={'display': 'flex', 'width': '40%',
                                'justify-content': 'center', 'align-items': 'center', 'objectFit': 'contain',
                                }, id='dashboard-profile-image'),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div("", id='dashboard-profile-name',
                                     style={'font-size': '1.1rem', 'font-weight': 'bold', 'text-align': 'center'}),
                            html.Div("", id='dashboard-profile-birth',
                                     style={'font-size': '1.1rem', 'font-weight': 'bold', 'text-align': 'center'}),
                        ], style={'width': '50%', 'display': 'flex',
                                  'justify-content': 'space-evenly', 'align-items': 'center',
                                  'height': '100%', 'flex-direction': 'column'}),
                        html.Div([
                            html.Div("", id='dashboard-profile-gender',
                                     style={'font-size': '1.1rem', 'font-weight': 'bold', 'text-align': 'center'}),
                            html.Div("", id='dashboard-profile-age',
                                     style={'font-size': '1.1rem', 'font-weight': 'bold', 'text-align': 'center'}),
                        ], style={'width': '50%', 'display': 'flex',
                                  'justify-content': 'space-evenly', 'align-items': 'center',
                                  'height': '100%', 'flex-direction': 'column'}),
                    ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center',
                              'width': '100%', 'height': '100%'}),
                ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center',
                          'width': '60%', 'padding': '0px 10px',
                          'background-color': 'rgba(37, 93, 201, 0.1)', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.25)',
                          'border-radius': '20px'}),
            ], style={'width': '100%', 'height': '15vh', 'flex-direction': 'row', 'display': 'flex'})
        ], className='d-flex justify-content-between align-items-center w-100'),

        dbc.Row([
            html.Div([
                html.Div(id='dashboard-slider-container', children=get_slides(),
                         style={'display': 'flex', 'transition': 'transform 0.5s ease',
                                'width': '300%', 'transform': 'translateX(0%)', 'height': '100%'}
                         ),
            ], style={'width': '100%', 'height': '15vh', 'justify-content': 'center',
                      'align-items': 'center', 'overflow': 'hidden',
                      'background-color': 'rgba(37, 93, 201, 0.1)', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.25)',
                      'border-radius': '20px', 'padding': '10px'}, ),

        ], className='d-flex justify-content-center align-items-center w-100 mt-4'),

        # dbc.Row([
        #     html.Div(
        #         [
        #         dcc.Graph(id='live-graph',
        #                    config={'displayModeBar': False},
        #                    style={'height': '100%', 'width': '100%'},
        #                    className='p-0'),
        #         dcc.Interval(
        #              id='graph-update',
        #              interval=1000,  # Update graph every second
        #              n_intervals=0
        #          ), ]
        #         , style={'width': '100%', 'height': '40vh', 'display': 'flex',})
        # ], className='d-flex justify-content-between align-items-center w-100 mt-4'),
    ], className="d-flex align-items-center flex-column mx-3 w-100")
    return content


def get_slides():
    slides = [
        html.I(className='ic-arrow-left-rounded', id='dashboard-slider-back-button-1',
               style={'width': '10%', 'height': '100%'}),
        html.Div(set_slide_content_1(),
                 style={'background-color': '#FFFFFF', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.25)',
                        'border-radius': '20px', 'width': '100%', 'height': '95%', }),
        html.I(className='ic-arrow-right-rounded', id='dashboard-slider-forward-button-1',
               style={'width': '10%', 'height': '100%'}),
        html.I(className='ic-arrow-left-rounded', id='dashboard-slider-back-button-2',
               style={'width': '10%', 'height': '100%'}),
        html.Div(set_slide_content_2(),
                 style={'background-color': '#FFFFFF', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.25)',
                        'border-radius': '20px', 'width': '100%', 'height': '95%'}),
        html.I(className='ic-arrow-right-rounded', id='dashboard-slider-forward-button-2',
               style={'width': '10%', 'height': '100%'}),
        html.I(className='ic-arrow-left-rounded', id='dashboard-slider-back-button-3',
               style={'width': '10%', 'height': '100%'}),
        html.Div(set_slide_content_3(),
                 style={'background-color': '#FFFFFF', 'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.25)',
                        'border-radius': '20px', 'width': '100%', 'height': '95%'}),
        html.I(className='ic-arrow-right-rounded', id='dashboard-slider-forward-button-3',
               style={'width': '10%', 'height': '100%'}),
    ]
    return slides


def set_slide_content_1():
    content = html.Div([
        html.Div(
            html.Img(style={'display': 'flex', 'width': '80%', 'height': '90%',
                            'justify-content': 'center', 'align-items': 'center', 'objectFit': 'contain',
                            }, src='../../../assets/img/Lying_down.svg'),
            style={'width': '30%', 'height': '100%', 'display': 'flex', 'justify-content': 'center',
                   'align-items': 'center'}),
        html.Div([
            html.Div([
                html.Div([
                    html.Div("활동상태",
                             style={'font-size': '0.9rem', 'font-weight': 'bold', 'text-align': 'center'}),
                    html.Div("누워있음",
                             style={'font-size': '0.9rem', 'font-weight': 'bold', 'text-align': 'center'}),

                ], style={'width': '100%', 'display': 'flex',
                          'justify-content': 'space-evenly', 'align-items': 'center',
                          'height': '100%', 'flex-direction': 'row'}),
                html.Div([
                    html.Div(id='dashboard-profile-status-lying-text',
                             style={'font-size': '0.9rem', 'font-weight': 'bold', 'text-align': 'center'}),
                    html.Div(id='dashboard-profile-status-lying-time',
                             style={'font-size': '0.9rem', 'font-weight': 'bold', 'text-align': 'center'}),
                ], style={'width': '100%', 'display': 'flex',
                          'justify-content': 'space-evenly', 'align-items': 'center',
                          'height': '100%', 'flex-direction': 'row'}),
            ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center',
                      'width': '100%', 'height': '100%', 'flex-direction': 'column'}),
        ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center',
                  'width': '70%', 'height': '100%'
                  }),
    ], style={'width': '100%', 'height': '100%', 'flex-direction': 'row', 'display': 'flex',
              'justify-content': 'center', 'align-items': 'center'})
    return content


def set_slide_content_2():
    content = html.Div([
        html.Div(
            html.Img(style={'display': 'flex', 'width': '80%', 'height': '90%',
                            'justify-content': 'center', 'align-items': 'center', 'objectFit': 'contain',
                            }, src='../../../assets/img/empty.svg'),
            style={'width': '30%', 'height': '100%', 'display': 'flex', 'justify-content': 'center',
                   'align-items': 'center'}),
        html.Div([
            html.Div([
                html.Div([
                    html.Div("활동상태",
                             style={'font-size': '0.9rem', 'font-weight': 'bold', 'text-align': 'center'}),
                    html.Div("비어있음",
                             style={'font-size': '0.9rem', 'font-weight': 'bold', 'text-align': 'center'}),

                ], style={'width': '100%', 'display': 'flex',
                          'justify-content': 'space-evenly', 'align-items': 'center',
                          'height': '100%', 'flex-direction': 'row'}),
                html.Div([
                    html.Div(id='dashboard-profile-status-empty-text',
                             style={'font-size': '0.9rem', 'font-weight': 'bold', 'text-align': 'center'}),
                    html.Div(id='dashboard-profile-status-empty-time',
                             style={'font-size': '0.9rem', 'font-weight': 'bold', 'text-align': 'center'}),
                ], style={'width': '100%', 'display': 'flex',
                          'justify-content': 'space-evenly', 'align-items': 'center',
                          'height': '100%', 'flex-direction': 'row'}),
            ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center',
                      'width': '100%', 'height': '100%', 'flex-direction': 'column'}),
        ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center',
                  'width': '70%', 'height': '100%'
                  }),
    ], style={'width': '100%', 'height': '100%', 'flex-direction': 'row', 'display': 'flex',
              'justify-content': 'center', 'align-items': 'center'})
    return content


def set_slide_content_3():
    content = html.Div([
        html.Div(
            html.Img(style={'display': 'flex', 'width': '80%', 'height': '90%',
                            'justify-content': 'center', 'align-items': 'center', 'objectFit': 'contain',
                            }, src='../../../assets/img/Sitting_down.svg'),
            style={'width': '30%', 'height': '100%', 'display': 'flex', 'justify-content': 'center',
                   'align-items': 'center'}),

        html.Div([
            html.Div([
                html.Div([
                    html.Div("활동상태",
                             style={'font-size': '0.9rem', 'font-weight': 'bold', 'text-align': 'center'}),
                    html.Div("앉아있음",
                             style={'font-size': '0.9rem', 'font-weight': 'bold', 'text-align': 'center'}),

                ], style={'width': '100%', 'display': 'flex',
                          'justify-content': 'space-evenly', 'align-items': 'center',
                          'height': '100%', 'flex-direction': 'row'}),
                html.Div([
                    html.Div(id='dashboard-profile-status-sitting-text',
                             style={'font-size': '0.9rem', 'font-weight': 'bold', 'text-align': 'center'}),
                    html.Div(id='dashboard-profile-status-sitting-time',
                             style={'font-size': '0.9rem', 'font-weight': 'bold', 'text-align': 'center'}),
                ], style={'width': '100%', 'display': 'flex',
                          'justify-content': 'space-evenly', 'align-items': 'center',
                          'height': '100%', 'flex-direction': 'row'}),
            ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center',
                      'width': '100%', 'height': '100%', 'flex-direction': 'column'}),
        ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center',
                  'width': '70%', 'height': '100%'
                  }),
    ], style={'width': '100%', 'height': '100%', 'flex-direction': 'row', 'display': 'flex',
              'justify-content': 'center', 'align-items': 'center'})
    return content
