from flask_restx import fields

sensitivity_model = {
    'userEmail': fields.String(required=True, description='User Email'),
    'targetStatus': fields.String(required=True, description='Target Status'),
    'weight': fields.Float(required=True, description='Weight'),
}