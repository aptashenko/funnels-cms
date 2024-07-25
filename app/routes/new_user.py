from app import db
from app.models import Users

def add_new_user(email, user_id):
    user = Users(email=email, web_user_id=user_id)
    db.session.add(user)
    db.session.commit()