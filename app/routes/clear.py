from app import db
from app.models import Users
def clear_all_users():
    db.session.query(Users).delete()
    db.session.commit()