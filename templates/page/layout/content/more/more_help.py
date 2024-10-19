import os

from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


def more_help_layout():

    layout = html.Div([
        dcc.Store(id='more-help-current-step-store', data=1),  # 데이터를 저장할 숨겨진 Store
        dbc.Container([
            html.Div(children=more_help_step_1_content(), id='more-help-main-content', className='w-100',
                     style={'height': '100vh'}),
        ], className='p-0'),

        # 하단 영역

    ], className="min-vh-100 d-flex flex-column bg-white")

    return layout


def get_step_content(step):
    if step == 1:
        return more_help_step_1_content()
    elif step == 2:
        return more_help_step_2_content()
    elif step == 3:
        return more_help_step_3_content()
    else:
        return ""


def more_help_step_1_content():
    # 콘텐츠 부분
    content = html.Div(
        [
            html.Div(style={'height': '40vh'}),  # 빈 공간
            html.Div([  # 화살표 버튼
                html.I(className='ic-arrow-forward-white', id='more-help-next-button',
                       style={'width': '10vh', 'height': '10vh',
                              'cursor': 'pointer'}),
            ], style={'height': '20vh', 'display': 'flex', 'align-items': 'center',
                      'justify-content': 'end'}),
            html.Div(  # 텍스트 콘텐츠
                html.Span(["BehaPulse는", html.Br(), "Wi-Fi sensing으로", html.Br(), "사용자의 상태를", html.Br(), "모니터링 합니다."],
                          style={'font-size': '3vh', 'color': 'white', 'font-weight': 'bold'}),
                style={'height': '30vh', 'display': 'flex', 'align-items': 'end', 'margin-left': '5vh'}),
        ],
        style={
            'position': 'relative',  # 상대 위치 설정
            'z-index': '1',  # 배경 위에 나타나도록 설정
            'height': '100%',  # 전체 높이
            'color': 'white'
        }
    )

    # 배경 이미지 및 필터 적용 레이어
    background = html.Div(
        style={
            'background': "url('../../../assets/img/help_1.png')",  # 배경 이미지 경로
            'background-size': 'cover',  # 배경 이미지 크기 설정
            'background-position': 'center',  # 배경 이미지 위치 설정
            'filter': 'brightness(40%)',  # 배경만 어둡게 처리
            'position': 'absolute',  # 절대 위치 지정
            'top': '0',
            'left': '0',
            'width': '100%',
            'height': '100%',
            'z-index': '0'  # 배경은 가장 뒤에 배치
        }
    )

    # 최종 레이아웃
    return html.Div([background, content], style={'position': 'relative', 'height': '100%'})

def more_help_step_2_content():
    # 콘텐츠 부분
    content = html.Div(
        [
            html.Div(style={'height': '40vh'}),  # 빈 공간
            html.Div([  # 화살표 버튼
                html.I(className='ic-arrow-forward-white', id='more-help-next-button',
                       style={'width': '10vh', 'height': '10vh',
                              'cursor': 'pointer'}),
            ], style={'height': '20vh', 'display': 'flex', 'align-items': 'center',
                      'justify-content': 'end'}),
            html.Div(  # 텍스트 콘텐츠
                html.Span(["BehaPulse는", html.Br(), "실시간 모니터링 서비스를", html.Br(), "제공합니다."],
                          style={'font-size': '3vh', 'color': 'white', 'font-weight': 'bold'}),
                style={'height': '30vh', 'display': 'flex', 'align-items': 'end', 'margin-left': '5vh'}),
        ],
        style={
            'position': 'relative',  # 상대 위치 설정
            'z-index': '1',  # 배경 위에 나타나도록 설정
            'height': '100%',  # 전체 높이
            'color': 'white'
        }
    )

    # 배경 이미지 및 필터 적용 레이어
    background = html.Div(
        style={
            'background': "url('../../../assets/img/help_2.png')",  # 배경 이미지 경로
            'background-size': 'cover',  # 배경 이미지 크기 설정
            'background-position': 'center',  # 배경 이미지 위치 설정
            'filter': 'brightness(40%)',  # 배경만 어둡게 처리
            'position': 'absolute',  # 절대 위치 지정
            'top': '0',
            'left': '0',
            'width': '100%',
            'height': '100%',
            'z-index': '0'  # 배경은 가장 뒤에 배치
        }
    )

    # 최종 레이아웃
    return html.Div([background, content], style={'position': 'relative', 'height': '100%'})

def more_help_step_3_content():
    # 콘텐츠 부분
    content = html.Div(
        [
            html.Div(style={'height': '40vh'}),  # 빈 공간
            html.Div([  # 화살표 버튼
                html.I(className='ic-arrow-forward-white', id='more-help-next-button',
                       style={'width': '10vh', 'height': '10vh',
                              'cursor': 'pointer'}),
            ], style={'height': '20vh', 'display': 'flex', 'align-items': 'center',
                      'justify-content': 'end'}),
            html.Div(  # 텍스트 콘텐츠
                html.Span(["BehaPulse는", html.Br(), "경량화된 설계와", html.Br(), "AI 기능이 탑재되어있는", html.Br(), "기기를 활용합니다."],
                          style={'font-size': '3vh', 'color': 'white', 'font-weight': 'bold'}),
                style={'height': '30vh', 'display': 'flex', 'align-items': 'end', 'margin-left': '5vh'}),
        ],
        style={
            'position': 'relative',  # 상대 위치 설정
            'z-index': '1',  # 배경 위에 나타나도록 설정
            'height': '100%',  # 전체 높이
            'color': 'white'
        }
    )

    # 배경 이미지 및 필터 적용 레이어
    background = html.Div(
        style={
            'background': "url('../../../assets/img/help_3.png')",  # 배경 이미지 경로
            'background-size': 'cover',  # 배경 이미지 크기 설정
            'background-position': 'center',  # 배경 이미지 위치 설정
            'filter': 'brightness(40%)',  # 배경만 어둡게 처리
            'position': 'absolute',  # 절대 위치 지정
            'top': '0',
            'left': '0',
            'width': '100%',
            'height': '100%',
            'z-index': '0'  # 배경은 가장 뒤에 배치
        }
    )

    # 최종 레이아웃
    return html.Div([background, content], style={'position': 'relative', 'height': '100%'})