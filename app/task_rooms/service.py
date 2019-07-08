from bson import ObjectId
from flask_restplus import abort
from flask_jwt_extended import get_jwt_identity
from app.task_rooms.models import room_request, room_record
from app.utils.db_utils import Base
from app.utils.helper import custom_marshal, update_timestamp
from app.common.constants import COLLECTIONS

base_obj = Base()


class TaskRoomService(object):
    """
    Service Class for Task
    """
    def create_room(self, payload):
        """
        Create Room for an User
        :param payload:
        :return:
        """
        payload = custom_marshal(payload, room_record, 'create')
        _id = base_obj.insert(COLLECTIONS['ROOMS'], payload)

    def get_rooms(self, email, state):
        """
        Get Rooms for a particular User
        :param email:
        :return:
        """
        if state == 'active':
            query = {"users": email, "meta.is_deleted": False, "meta.is_archived": False}
        elif state == 'archived':
            query = {"users": email, "meta.is_archived": True}
        elif state == 'deleted':
            query = {"users": email, "meta.is_deleted": True}

        count, records = base_obj.get(COLLECTIONS['ROOMS'], query)
        return records

    def update_room(self, id, payload):
        """
        Update Room
        :param payload:
        :return:
        """
        payload = custom_marshal(payload, room_request, 'update')
        email = get_jwt_identity()
        result = base_obj.update(COLLECTIONS['ROOMS'], {"_id": ObjectId(id), "meta.created_by": email}, {"$set": payload})
        print(result.modified_count)
        if not result.modified_count:
            abort(401, "Unauthorized")

    def archive_room(self, id):
        """
        Archive Room
        :param payload:
        :return:
        """
        payload = update_timestamp()
        email = get_jwt_identity()
        payload["meta.is_archived"], payload["meta.is_deleted"] = True, False
        result = base_obj.update(COLLECTIONS['ROOMS'], {"_id": ObjectId(id), "meta.created_by": email},
                        {"$set": payload})
        if not result.modified_count:
            abort(401, "Unauthorized")

    def delete_room(self, id):
        """
        Delete Room
        :param payload:
        :return:
        """
        payload = update_timestamp()
        email = get_jwt_identity()
        payload["meta.is_archived"], payload["meta.is_deleted"] = False, True
        result = base_obj.update(COLLECTIONS['ROOMS'], {"_id": ObjectId(id), "meta.created_by": email},
                        {"$set": payload})
        if not result.modified_count:
            abort(401, "Unauthorized")

    def change_status(self, id):
        """
        Change Status to Active
        :param id:
        :return:
        """
        payload = update_timestamp()
        email = get_jwt_identity()
        payload["meta.is_archived"], payload["meta.is_deleted"] = False, False
        result = base_obj.update(COLLECTIONS['ROOMS'], {"_id": ObjectId(id), "meta.created_by": email},
                        {"$set": payload})
        if not result.modified_count:
            abort(401, "Unauthorized")

    def invite_user(self, id, email):
        """
        Invite User to the task room
        :param id:
        :param payload:
        :return:
        """
        email = get_jwt_identity()
        count, records = base_obj.get(COLLECTIONS['USERS'], {'email': user_email, "meta.is_deleted": False})
        if count == 1:
            if records[0]['is_active']:
                result = base_obj.update(COLLECTIONS['ROOMS'], {"_id": ObjectId(id), "meta.created_by": email},
                                {"$push": {'users': user_email}})
                if not result.modified_count:
                    abort(401, "Unauthorized")
            else:
                abort(401, "Email ID is not active")
        else:
            abort(404, "Email ID does not exist")

    def exit_task_room(self, id, email):
        """
        Exit from a task room
        :param id:
        :param email:
        :return:
        """
        base_obj.update(COLLECTIONS['ROOMS'], {"_id": ObjectId(id)},
                        {"$pull": {'users': email}})