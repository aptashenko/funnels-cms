import random
from app.models import Promocodes
from app import db
from datetime import datetime, timedelta



def get_random_promocode():
    promocodes = Promocodes.query.filter_by(user_email=None).all()
    promocode = random.choice(promocodes)
    return promocode.value

def reset_all_promocodes():
    promocodes = Promocodes.query.all();
    for promocode in promocodes:
        promocode.user_email = None
        promocode.used = 0
        promocode.created_at = None
    db.session.commit()

def reset_expired_promocodes(database):
    now = datetime.now()
    one_day_ago = now - timedelta(days=1)

    promocodes_with_date = Promocodes.query.filter(Promocodes.created_at.isnot(None), Promocodes.used == 0).all()

    for promocode in promocodes_with_date:
        if promocode.created_at <= one_day_ago:
            promocode.user_email = None
            promocode.created_at = None

    database.session.commit()