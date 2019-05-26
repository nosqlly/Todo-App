from flask_restplus import fields
from app import api
from app.common.models import meta

user_base = api.model('signup',{
    'email': fields.String(description="Email ID"),
    'first_name': fields.String(description="First Name"),
    'last_name': fields.String(description="Last Name"),
    'password': fields.String(description="Password")
})

user_request = api.inherit('user base', user_base, {
    'confirm_password': fields.String(description="Confirm password")
})

user = api.inherit('user', user_base, {
    'is_active': fields.Boolean(default=False, description="Account Activated or Not"),
    'meta': fields.Nested(meta)
})
