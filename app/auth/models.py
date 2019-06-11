from app import api
from flask_restplus import fields

login = api.model('login',{
    'email': fields.String(required=True, description="Enter Email ID"),
    'password': fields.String(required=True, description="Enter Password")
})
