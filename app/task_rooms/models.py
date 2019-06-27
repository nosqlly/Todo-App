from flask_restplus import fields, reqparse
from app import api
from app.common.models import meta
from app.task_rooms.tasks.models import task_response


state_parser = reqparse.RequestParser()
state_parser.add_argument('State', type=str, location='args')

room_request = api.model('room_request', {
    'room_name': fields.String(required=True, description="Room name")
})

meta_tasks = api.inherit('meta_tasks', meta, {
    "is_archived": fields.Boolean(default=False)
})

room_record = api.inherit('room_record', room_request, {
    'users': fields.List(fields.String),
    'tasks': fields.List(fields.Nested(task_response)),
    'meta': fields.Nested(meta_tasks)
})

room_response = api.inherit('room_response', room_record, {
    '_id': fields.String()
})

invite_user = api.model('invite_user', {
    'email': fields.String(required=True, description='Enter Email ID')
})
