from flask_restplus import fields, reqparse
from app import api
from app.utils.date_utils import get_current_time

meta = api.model('meta', {
    'is_deleted': fields.Boolean(default=False),
    'created_on': fields.DateTime(default=get_current_time()),
    'updated_on': fields.DateTime(default=get_current_time()),
    'created_by': fields.String(default='user'),
    'updated_by': fields.String(default='user')
})

auth_parser = reqparse.RequestParser()
auth_parser.add_argument('Authorization', location='headers')
