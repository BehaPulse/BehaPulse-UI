from .signup import *
from .splash import *
from .login import *
from .content import *
from .find_id import *
from .find_pw import *

from dash.dependencies import Input, Output

url_to_layout = {
    '/beha-pulse/': splash_layout,
    '/beha-pulse/signup/': signup_layout,
    '/beha-pulse/login/': login_layout,
    '/beha-pulse/find-id/': find_id_layout,
    '/beha-pulse/find-password/': find_pw_layout,
}
main_layout_content = {
    '/beha-pulse/main/sensitivity/': main_sensitivity_layout,
}
device_layout_content = {
    '/beha-pulse/main/device/add/': device_add_layout,
    '/beha-pulse/main/device/edit/': device_edit_layout,
    '/beha-pulse/main/device/detail/': device_detail_layout,
}

control_layout_content = {
    '/beha-pulse/main/control/setting/': control_setting_layout,
    '/beha-pulse/main/control/color/': control_color_layout,
}

dashboard_layout_content = {
    '/beha-pulse/main/dashboard/add/': dashboard_add_layout,
    '/beha-pulse/main/dashboard/delete/': dashboard_delete_layout,
    '/beha-pulse/main/dashboard/not-connected/': dashboard_not_connected_layout,
    '/beha-pulse/main/dashboard/detail/': dashboard_detail_layout,
}

more_layout_content = {
    '/beha-pulse/main/more/privacy-policy/': more_privacy_layout,
    '/beha-pulse/main/more/document/': more_document_layout,
    '/beha-pulse/main/more/information/': more_info_layout,
    '/beha-pulse/main/more/help/': more_help_layout,
    '/beha-pulse/main/more/password/': more_password_change_layout,
    '/beha-pulse/main/more/sensitivity/': more_sensitivity_layout,
    '/beha-pulse/main/more/smart-things/': more_smart_things_layout,
}


tab_to_layout = {
    '/beha-pulse/main/': main_layout,
    '/beha-pulse/main/device/': device_layout,
    '/beha-pulse/main/control/': control_layout,
    '/beha-pulse/main/dashboard/': dashboard_layout,
    '/beha-pulse/main/more/': more_layout,
}

not_need_login_layout = [
    '/beha-pulse/',
    '/beha-pulse/signup/',
    '/beha-pulse/login/',
    '/beha-pulse/find-id/',
    '/beha-pulse/find-password/',
]


def set_layout(app):
    @app.callback(
        [Output('page', 'children'),
         Output('redirect', 'href', allow_duplicate=True)],
        [Input('url', 'pathname')],
        prevent_initial_call=True
    )
    def display_page(pathname):
        layout = html.Div()
        redirect_url = None

        if not session.get('login'):  # 로그인이 되어 있지 않은 경우
            if pathname in not_need_login_layout:  # 로그인 없이 이용할 수 있는 경우
                layout = url_to_layout.get(pathname, splash_layout)()

            else:  # 반드시 로그인이 필요한 레이아웃의 경우,
                redirect_url = '/beha-pulse/login/'

        else:  # 로그인 되어 있는 경우
            # 로그인이 되어있는 데 로그인이 필요없는 레이아웃을 요청하는 경우
            if pathname in not_need_login_layout:
                redirect_url = '/beha-pulse/main/'

            else:  # 로그인이 되어 있는 데 로그인이 필요한 레이아웃을 요청한 경우
                if pathname in tab_to_layout:
                    print(0)
                    layout = tab_to_layout.get(pathname)()
                elif pathname in main_layout_content:
                    print(1)
                    layout = main_layout_content.get(pathname)()
                elif pathname in device_layout_content:
                    print(2)
                    layout = device_layout_content.get(pathname)()
                elif pathname in control_layout_content:
                    print(3)
                    layout = control_layout_content.get(pathname)()
                elif pathname in dashboard_layout_content:
                    print(4)
                    layout = dashboard_layout_content.get(pathname)()
                elif pathname in more_layout_content:
                    print(5)
                    layout = more_layout_content.get(pathname)()

                else:  # 로그인이 되어있는 데, 정해지지 않은 URL로 요청한 경우
                    redirect_url = '/beha-pulse/main/'
        print(session)
        return layout, redirect_url
