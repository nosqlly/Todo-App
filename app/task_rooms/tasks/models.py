from flask_restplus import fields, reqparse
from app import api
from app.common.models import meta


state_parser = reqparse.RequestParser()
state_parser.add_argument('State', type=str, location='args')

meta_tasks = api.inherit('meta_tasks', meta, {
    "is_archived": fields.Boolean(default=False)
})

task_request = api.model('task_request', {
    'task_name': fields.String(required=True),
    'task_data': fields.String()
})

task_db_input = api.inherit('task_db_input', task_request, {
    'meta': fields.Nested(meta_tasks)
})

task_response = api.inherit('task_response', task_db_input, {
    '_id': fields.String()
})


