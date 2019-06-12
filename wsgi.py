from app import application, api
from app.users.views import users_ns
from app.auth.views import auth_ns
from app.task_rooms.views import taskrooms_ns

api.add_namespace(users_ns, '/api/v1/users')
api.add_namespace(auth_ns, '/api/v1/auth')
api.add_namespace(taskrooms_ns, '/api/v1/task_rooms')

if __name__ == '__main__':
    application.run(host='0.0.0.0')

