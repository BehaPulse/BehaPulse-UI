from flask import Flask, session
from dash import Dash, dcc, html

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


def more_document_layout():
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
                        html.Span("이용약관",
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
            html.Span("Behapulse Behapulse 이용약관",
                      style={'font-size': '1.25rem', 'font-weight': 'bold', 'padding': '0px'}),
            html.Span("제1장 총칙", style={'font-weight': 'bold', 'padding': '0px', 'margin-top': '10px'}),
            html.Span("제1조 (목적)", style={'padding-left': '10px', 'padding-right': '0px'}),
            html.Span(
                "이 약관은 Behapulse(이하 “베하”라 합니다)가 모바일 기기를 통해 제공 하는 게임 서비스 및 이에 부수하는 네트워크, 웹사이트, 기타 서비스(이하 “서비스” 라 합니다)의 이용에 대한 베하와 서비스 이용자의 권리ㆍ의무 및 책임사항, 기타 필요 한 사항을 규정함을 목적으로 합니다.",
                style={'padding-left': '10px', 'padding-right': '0px'}),
            html.Span("제2조 (용어의 정의)", style={'padding-left': '10px', 'padding-right': '0px', 'margin-top': '10px'}),
            html.Span(
                "① 이 약관에서 사용하는 용어의 정의는 다음과 같습니다. 1. “베하”라 함은 모바일 기기를 통하여 서비스를 제공하는 사업자를 의미합니다. 2. “회원”이란 이 약관에 따라 이용계약을 체결하고, 베하가 제공하는 서비스를 이 용하는 자를 의미합니다. 3. “모바일 기기”란 콘텐츠를 다운로드 받거나 설치하여 사용할 수 있는 기기로서, 휴대폰, 스마트폰, 휴대정보단말기(PDA), 태블릿 등을 의미합니다. 4. “애플리케이션”이란 베하가 제공하는 서비스를 이용하기 위하여 모바일 기기를 통해 다운로드 받거나 설치하여 사용하는 프로그램 일체를 의미합니다.",
                style={'padding-left': '10px', 'padding-right': '0px'}),
            html.Span("제2장 이용계약 당사자의 의무", style={'font-weight': 'bold', 'padding': '0px', 'margin-top': '10px'}),
            html.Span("제3조 (회원의 의무)", style={'padding-left': '10px', 'padding-right': '0px'}),
            html.Span(
                "① 회원의 계정 및 모바일 기기에 관한 관리 책임은 회원에게 있으며, 이를 타인이 이 용하도록 하게 하여서는 안 됩니다. 모바일 기기의 관리 부실이나 타인에게 이용을 승 낙함으로 인해 발생하는 손해에 대해서 베하는 책임을 지지 않습니다.",
                style={'padding-left': '10px', 'padding-right': '0px'}),
            html.Span("제3장 서비스 이용 및 이용제한", style={'font-weight': 'bold', 'padding': '0px', 'margin-top': '10px'}),
            html.Span("제4조 (서비스의 이용)", style={'padding-left': '10px', 'padding-right': '0px'}),
            html.Span(
                "① 다운로드하여 설치한 애플리케이션 또는 네트워크를 통해 이용하는 서비스의 경우 에는 백그라운드 작업이 진행될 수 있습니다. 이 경우 모바일 기기 또는 이동통신사의 특성에 맞도록 추가요금이 발생할 수 있으며 이와 관련하여 베하는 책임을 지지 않습니다.",
                style={'padding-left': '10px', 'padding-right': '0px'}),
            html.Span("제4장 (이용제한 조치에 대한 이의신청 절차)",
                      style={'font-weight': 'bold', 'padding': '0px', 'margin-top': '10px'}),
            html.Span(
                "① 회원이 베하의 이용제한 조치에 불복하고자 할 때에는 이 조치의 통지를 받은 날부터 14일 이내에 불복 이유를 기재한이의 신청서를 서면, 전자우편 또는 이에 준하는 방법으로 베하에 제출하여야 합니다. ② 베하는 제1항의 이의신청서를 접수한 날부터 15일 이내에 불복 이유에 대하여서면, 전자우편 또는 이에 준하는 방법으로 답변합니다. 다만, 베하는 이 기간 내에답변이 어려운 경우에는 그 사유와 처리일정을 통지합니다. ③ 애플리케이션의 다운로드 또는 네트워크 서비스의 이용으로 인해 발생한 통신요금 (통화료, 데이터 통화료 등)은 환급 대상에서 제외될 수 있습니다",
                style={'padding-left': '10px', 'padding-right': '0px'}),
            html.Span("제5장 청약철회, 과오납금의 환급 및 이용계약의 해지",
                      style={'font-weight': 'bold', 'padding': '0px', 'margin-top': '10px'}),
            html.Span("제5조 (계약 해지 등)", style={'padding-left': '10px', 'padding-right': '0px'}),
            html.Span(
                "① 베하는 최근의 서비스 이용일부터 연속하여 1년 동안 베하의 서비스를 이용하지않은 회원(이하 “휴면계정”이라 합니다)의 개인정보를 보호하기 위해 이용계약을해지하고 회원의 개인정보 파기 등의 조치를 취할 수 있습니다. 이 경우 조치일 30일전까지 계약해지, 개인정보 파기 등의 조치가 취해진다는 사실 및 파기될 개인정보등을회원에게 통지합니다..",
                style={'padding-left': '10px', 'padding-right': '0px'}),
            html.Span("제6장 손해배상 및 면책조항 등", style={'font-weight': 'bold', 'padding': '0px', 'margin-top': '10px'}),
            html.Span("제6조 (손해배상)", style={'padding-left': '10px', 'padding-right': '0px'}),
            html.Span(
                "① 회원이 서비스와 관련하여 게재한 정보나 자료 등의 신뢰성, 정확성 등에 대하여 베하는 고의 또는 중대한 과실이 없는 한 책임을 지지 않습니다. ② 베하는 회원이 다른 회원 또는 타인과 서비스를 매개로 발생한 거래나 분쟁에 대해 개입할 의무가 없으며, 이로 인한 손해에 대해 책임을 지지 않습니다.",
                style={'padding-left': '10px', 'padding-right': '0px'}),

            html.Span("제7조(회사의 면책)", style={'padding-left': '10px', 'padding-right': '0px','margin-top': '10px'}),
            html.Span(
                "③ 베하는 무료로 제공되는 서비스 이용과 관련하여 회원에게 발생한 손해에 대해서는 책임을 지지 않습니다. 그러나 베하의 고의 또는 중과실에 의한 경우에는 그러하지 아 니합니다.",
                style={'padding-left': '10px', 'padding-right': '0px'}),
            html.Span(
                "④ 회원이 모바일 기기의 변경, 모바일 기기의 번호 변경, 운영체제(OS) 버전의 변경, 해외 로밍, 통신사 변경 등으로 인해 콘텐츠 전부나 일부의 기능을 이용할 수 없는 경 우 베하는 이에 대해 책임을 지지 않습니다. 다만, 베하의 고의 또는 과실에 의한 경우 에는 그러하지 아니합니다.",
                style={'padding-left': '10px', 'padding-right': '0px'}),

            html.Span("제8조 (회원에 대한 통지)", style={'padding-left': '10px', 'padding-right': '0px','margin-top': '10px'}),
            html.Span("① 베하가 회원에게 통지를 하는 경우 회원의 전자우편주소, 전자메모, 게임 서비스 내 쪽지, 문자메시지(LMS/SMS) 등으로 할 수 있습니다.",
                      style={'padding-left': '10px', 'padding-right': '0px'}),

        ], className="w-100 p-0"),

    ], className="d-flex align-items-center flex-column mx-3 w-100")
    return content
