from app import db
from app.models import Promocodes
def use_promocode(value):
    promocode = Promocodes.query.filter_by(value=value).first()
    if not promocode:
        return {'status': 404, 'message': {'error': 'Промокод не найден'}}
    if promocode.used == 1:
        return {'status': 409, 'message': {'error': 'Этот промокод уже использован'}}

    promocode.used = 1
    db.session.commit()
    return {'status': 200, 'message': {'success': f'Промокод {value} успешно активирован'}}