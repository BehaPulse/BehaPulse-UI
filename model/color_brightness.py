from flask_restx import fields

color_brightness_model = {
    'color': fields.String(description='Color', required=True),
    'brightness': fields.Integer(description='Brightness', required=True),
    'status': fields.String(description='Status', required=True),
    'personId': fields.Integer(description='Person ID', required=True),
}
