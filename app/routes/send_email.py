from app import db
from app.models import Promocodes, Users
from app.services import get_random_promocode
from selzy.send_email import send_message
from datetime import datetime
def send_email(email):
    user = Users.query.filter_by(email=email).first()
    if not user:
        return {'status': 404, 'message': {'User not found'}}

    promocode_value = get_random_promocode()
    promocode = Promocodes.query.filter_by(value=promocode_value).first()
    promocode.user_email = email
    promocode.created_at = datetime.utcnow()
    user.promocode_id = promocode_value
    send_message(user.email, promocode_value)
    db.session.commit()
    return {'status': 200, 'message': {'promocode': promocode_value}}