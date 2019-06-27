from bson import ObjectId
from app.task_rooms.tasks.models import task_db_input, task_request
from app.utils.db_utils import Base
from app.utils.helper import custom_marshal, update_timestamp
from app.common.constants import COLLECTIONS

base_obj = Base()


class TasksService(object):
    """
    Tasks Service
    """
    def get_tasks(self, id, state):
        """
        Get Tasks list
        :param id:
        :return:
        """
        if state == 'active':
            cond = {"$and": [{"$eq": ["$$task.meta.is_archived", False]}, {"$eq": ["$$task.meta.is_deleted", False]}]}
        elif state == 'archived':
            cond = {"$and": [{"$eq": ["$$task.meta.is_archived", True]}, {"$eq": ["$$task.meta.is_deleted", False]}]}
        elif state == 'deleted':
            cond = {"$and": [{"$eq": ["$$task.meta.is_archived", False]}, {"$eq": ["$$task.meta.is_deleted", True]}]}
        query = [{"$match": {"_id": ObjectId(id)}},
                 {"$project":
                      {"tasks": {"$filter": {"input": "$tasks", "as": "task", "cond": cond}}}}]
        records = base_obj.aggregate(COLLECTIONS['ROOMS'], query)
        tasks = records[0]['tasks']
        return tasks

    def create_task(self, id, payload):
        """
        Create a task in task room
        :param payload:
        :return:
        """
        payload = custom_marshal(payload, task_db_input, 'create')
        payload['_id'] = ObjectId()
        result = base_obj.update(COLLECTIONS['ROOMS'], {'_id': ObjectId(id)},
                                 {"$push": {'tasks': payload}})

    def update_task(self, taskroom_id, task_id, payload):
        """
        Update the task id with payload
        :param taskroom_id:
        :param task_id:
        :param payload:
        :return:
        """
        payload = custom_marshal(payload, task_request, 'update', prefix="tasks.$")
        result = base_obj.update(COLLECTIONS['ROOMS'], {'_id': ObjectId(taskroom_id), "tasks._id": ObjectId(task_id)},
                                 {"$set": payload})
        print(payload, result)

    def archive_task(self, taskroom_id, task_id):
        """
        Update the task id with payload
        :param taskroom_id:
        :param task_id:
        :param payload:
        :return:
        """
        payload = update_timestamp(prefix="tasks.$")
        payload["tasks.$.meta.is_archived"], payload["tasks.$.meta.is_deleted"] = True, False
        result = base_obj.update(COLLECTIONS['ROOMS'], {'_id': ObjectId(taskroom_id), "tasks._id": ObjectId(task_id)},
                                 {"$set": payload})
        print(payload, result)

    def delete_task(self, taskroom_id, task_id):
        """
        Update the task id with payload
        :param taskroom_id:
        :param task_id:
        :param payload:
        :return:
        """
        payload = update_timestamp(prefix="tasks.$")
        payload["tasks.$.meta.is_archived"], payload["tasks.$.meta.is_deleted"] = False, True
        result = base_obj.update(COLLECTIONS['ROOMS'], {'_id': ObjectId(taskroom_id), "tasks._id": ObjectId(task_id)},
                                 {"$set": payload})
        print(payload, result)

    def undo_task(self, taskroom_id, task_id):
        """
        Update the task id with payload
        :param taskroom_id:
        :param task_id:
        :param payload:
        :return:
        """
        payload = update_timestamp(prefix="tasks.$")
        payload["tasks.$.meta.is_archived"], payload["tasks.$.meta.is_deleted"] = False, False
        result = base_obj.update(COLLECTIONS['ROOMS'], {'_id': ObjectId(taskroom_id), "tasks._id": ObjectId(task_id)},
                                 {"$set": payload})
        print(payload, result)