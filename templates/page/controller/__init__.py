def set_controller(app):
    from .signup import signup_controller
    from .login import login_controller
    from .main import main_bottom_controller
    from .find_id import find_id_controller
    from .find_pw import find_pw_controller

    from .device import device_controller
    from .dashboard import dashboard_controller
    from .more import more_controller
    from .control import control_controller

    signup_controller(app)
    login_controller(app)
    main_bottom_controller(app)
    find_id_controller(app)
    find_pw_controller(app)

    device_controller(app)
    dashboard_controller(app)
    more_controller(app)
    control_controller(app)