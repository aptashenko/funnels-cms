from app.models import Users
from collections import OrderedDict

def get_users():
    users = Users.query.all()
    return [OrderedDict([('id', user.id), ('email', user.email), ('user_id', user.user_id), ('promocode_id', user.promocode_id), ('created_at', user.created_at)]) for user in users]