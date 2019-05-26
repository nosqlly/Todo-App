from flask_restplus import marshal
from app.utils.date_utils import get_current_time


def custom_marshal(model, template, option='create'):
    data = marshal(model, template)
    if option == 'create':
        data['meta']['created_on'] = get_current_time()
        data['meta']['updated_on'] = get_current_time()
    elif option == 'update' or option == 'delete':
        data['meta']['updated_on'] = get_current_time()
    return data
