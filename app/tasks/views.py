from flask_restplus import Namespace, Resource, marshal
from flask_jwt_extended import jwt_required
from app import api
from app.tasks.models import room_request, state_parser, room_response
from app.tasks.service import TaskService
from app.common.models import auth_parser
from flask_jwt_extended import get_jwt_identity

tasks_ns = Namespace('task', description="Room and todo task operations")

tasks_service = TaskService()


@tasks_ns.expect(auth_parser)
@tasks_ns.route('/rooms')
class Rooms(Resource):
    """
    Create and Get Rooms
    """
    @jwt_required
    @tasks_ns.expect(room_request)
    def post(self):
        """
        Create A Room
        :return:
        """
        email = get_jwt_identity()
        payload = api.payload
        payload['users'] = [email]
        tasks_service.create_room(payload)
        return {'Message': "Room created successfully"}

    @tasks_ns.expect(state_parser)
    @jwt_required
    def get(self):
        """
        Get Active, Archived and Deleted Rooms
        :return:
        """
        email = get_jwt_identity()
        args = state_parser.parse_args()
        if self.validate_state(args['State']):
            response = tasks_service.get_rooms(email, state=args['State'])
            return {'Message': "Rooms rendered successfully", 'records': marshal(response, room_response)}
        else:
            return {"Message": "State is not in (active|archived|deleted)"}

    @staticmethod
    def validate_state(state):
        if state == 'active' or state == 'archived' or state == 'deleted':
            return True
        else:
            return False

@tasks_ns.expect(auth_parser)
@tasks_ns.route('/rooms/<string:id>')
class RoomOperations(Resource):
    """
    Edit and Delete Rooms
    """

    @jwt_required
    @tasks_ns.expect(room_request)
    def put(self, id):
        """
        Edit a Room Name
        :param id:
        :return:
        """
        payload = api.payload
        tasks_service.update_room(id, payload)
        return {'Message': "Room updated successfully"}

@tasks_ns.expect(auth_parser)
@tasks_ns.route('/rooms/archive/<string:id>')
class RoomOperations(Resource):
    """
    Archive a room
    """

    @jwt_required
    def put(self, id):
        """
        Archive a Room Name
        :param id:
        :return:
        """
        tasks_service.archive_room(id)
        return {'Message': "Room archived successfully"}


@tasks_ns.expect(auth_parser)
@tasks_ns.route('/rooms/delete/<string:id>')
class RoomOperations(Resource):
    """
    Delete Rooms
    """

    @jwt_required
    def delete(self, id):
        """
        Delete Room
        :param id:
        :return:
        """
        tasks_service.delete_room(id)
        return {'Message': "Room deleted successfully"}


@tasks_ns.expect(auth_parser)
@tasks_ns.route('/rooms/undo/<string:id>')
class RoomOperations(Resource):
    """
    Move Rooms to Active Status
    """

    @jwt_required
    def put(self, id):
        """
        Move Rooms to Active Status
        :param id:
        :return:
        """
        tasks_service.change_status(id)
        return {'Message': "Room status changed to Active"}
