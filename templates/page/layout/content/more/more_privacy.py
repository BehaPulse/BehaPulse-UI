from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


def more_privacy_layout():
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
                        html.Span("개인정보 처리 방침",
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
            html.Div(children=more_privacy_content(), id='main-content', className='d-flex w-100',
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


def more_privacy_content():
    content = html.Div([
        dbc.Row([
            html.Span("Behapulse 개인정보 처리방침", style={'font-size': '1.25rem', 'font-weight': 'bold', 'padding': '0px'}),
            html.Div("Behapulse(이하 베하펄스)는 고객님의 개인정보를 중요시하며, \"정보통신망 이용촉진 및 정보보호\"에 관한 법률을 준수하고 있습니다. "
                     "Behapulse(이하 베하펄스)는 개인정보취급방침을 통하여 고객님께서 제공하시는 개인정보가 어떠한 용도와 방식으로 이용되고 있으며, "
                     "개인정보보호를 위해 어떠한 조치가 취해지고 있는지 알려드립니다.", className='mt-2 p-0'),
            html.Div("관계 법령 및 개인정보 취급방침에 따라 사용자 개인정보 보호에 최선을 다합니다.", className='p-0', style={'text-indent': '10px'}),
            html.Hr(style={'border-top': '1px solid #3F4F4F', 'width': '100%', 'margin': '20px 0px'}),
        ], className="w-100 p-0"),

        dbc.Row([
            html.Span("가. 수집하는 개인정보의 항목 및 수집방법", style={'font-weight': 'bold', 'padding': '0px', 'margin-top': '10px'}),
            html.Span("Behapulse(이하 베하펄스 은 개인을 식별할 수 있는 개인정보를 수집하지 않습니다.", style={'padding-left': '10px'}),
            html.Span("광고 식별자는 미 영구적이고 비 개인적인 식별자로써 개인을 식별할 수 없으며 식별한 정보를 별도로 수집, 보관 하지 않습니다.",
                      style={'padding-left': '10px', 'padding-right': '0px'}),
            html.Span("나. 개인정보의 수집 및 이용목적메세지", style={'font-weight': 'bold', 'padding': '0px', 'margin-top': '10px'}),
            html.Span("Behapulse(이하 베하펄스)는 개인정보를 수집하지 않습니다.", style={'padding-left': '10px', 'padding-right': '0px'}),
            html.Span("다. 개인정보 제공 및 공유", style={'font-weight': 'bold', 'padding': '0px', 'margin-top': '10px'}),
            html.Span("Behapulse(이하 베하펄스)는 개인정보를 공유 및 제3자에게 제공하지 않습니다.",
                      style={'padding-left': '10px', 'padding-right': '0px'}),
            html.Span("라. 수집한 개인정보의 취급 위탁", style={'font-weight': 'bold', 'padding': '0px', 'margin-top': '10px'}),
            html.Span("Behapulse(이하 베하펄스)는 개인정보를 수집, 이용, 보유하지 않습니다.",
                      style={'padding-left': '10px', 'padding-right': '0px'}),
            html.Span("마. 개인정보의 보유 및 이용기간", style={'font-weight': 'bold', 'padding': '0px', 'margin-top': '10px'}),
            html.Span("Behapulse(이하 베하펄스) 앱은 보유할 개인정보가 없습니다.", style={'padding-left': '10px', 'padding-right': '0px'}),
            html.Span("바. 개인정보 파기절차 및 방법", style={'font-weight': 'bold', 'padding': '0px', 'margin-top': '10px'}),
            html.Span("Behapulse(이하 베하펄스) 앱은 파기할 개인정보가 없습니다.", style={'padding-left': '10px', 'padding-right': '0px'}),
            html.Span("사. 개인정보 자동 수집 장치의 설치․운영 및 거부에 관한 사항", style={'font-weight': 'bold', 'padding': '0px', 'margin-top': '10px'}),
            html.Span("Behapulse(이하 베하펄스) 앱은 개인정보 자동 수집 장치를 운영하지 않습니다.",
                      style={'padding-left': '10px', 'padding-right': '0px'}),
            html.Span("아. 개인정보관리책임자", style={'font-weight': 'bold', 'padding': '0px', 'margin-top': '10px'}),
            html.Span(
                "Behapulse(이하 베하펄스) 앱은 고객의 개인정보를 보호하고 개인정보와 관련한 불만을 처리하기 위하여 아래와 같이 관련 부서 및 개인정보관리책임자를 지정하고 있습니다.",
                style={'padding-left': '10px', 'padding-right': '0px'}),
            html.Span("성명: 표지성, 문정곤, 이재훈, 이윤서, 윤지석", style={'padding-left': '10px', 'padding-right': '0px'}),
            html.Span("직책: Behapulse 개발자", style={'padding-left': '10px', 'padding-right': '0px'}),
            html.Span("귀하께서는 Behapulse의 서비스를 이용하시며 발생하는 모든 개인정보보호 관련 민원을 개인정보관리책임자에게 신고하실 수 있습니다.",
                      style={'padding-left': '10px', 'padding-right': '0px'}),
            html.Span("앱은 이용자들의 신고사항에 대해 신속하게 충분한 답변을 드릴 것입니다. 기타 개인정보침해에 대한 신고나 상담이 필요하신 경우에는 아래 기관에 문의하시기 바랍니다.",
                      style={'padding-left': '10px', 'padding-right': '0px'}),
            html.Span("1.개인분쟁조정위원회 (www.1336.or.kr/1336)", style={'padding-left': '10px', 'padding-right': '0px'}),
            html.Span("2.정보보호마크인증위원회 (www.eprivacy.or.kr/02–580–0533~4)",
                      style={'padding-left': '10px', 'padding-right': '0px'}),
            html.Span("3.대검찰청 인터넷범죄수사센터 (http://icic.sppo.go.kr/02–3480–3600)",
                      style={'padding-left': '10px', 'padding-right': '0px'}),
            html.Span("4.경찰청 사이버테러대응센터 (www.ctrc.go.kr/02–392–0330)",
                      style={'padding-left': '10px', 'padding-right': '0px'}),

        ], className="w-100 p-0")

    ], className="d-flex align-items-center flex-column mx-3 w-100")
    return content
