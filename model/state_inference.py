from flask_restx import fields

state_inference_model = {
    'personId': fields.Integer(required=True, description='Person Name'),
    'inferenceTime': fields.DateTime(required=True, description='Inference Time'),
    'inferencedStatus': fields.String(required=True, description='Inferenced Status'),
}
