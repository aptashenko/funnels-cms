from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
from collections import OrderedDict
from selzy.send_email import send_message
from selzy.send_support import support_email
import json
import random


MYSQL_HOST = 'ovh6.mirohost.net'
MYSQL_USER = 'u_aptashenko'
MYSQL_PASSWORD = 'Aptashenko93'
MYSQL_DB = 'utprozorro_db'

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), nullable=False)
    promocode_id = db.Column(db.String(20), nullable=True)
    web_user_id = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Promocodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(100), nullable=False)
    used = db.Column(db.Boolean, default=False)
    user_email = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)

@app.route('/add-user', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data or 'email' not in data:
        return Response(json.dumps({'error': 'Email is required'}), status=400, mimetype='application/json')
    if 'web_user_id' not in data:
        return Response(json.dumps({'error': 'web_user_id is required'}), status=400, mimetype='application/json')
    email = data['email']
    user_id = data['web_user_id']
    user = Users(email=email, web_user_id=user_id)

    try:
        db.session.add(user)
        db.session.commit()
        return Response(json.dumps({'message': 'User added successfully'}), mimetype='application/json')
    except Exception as e:
        db.session.rollback()
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()
    if not data or 'email' not in data:
        return Response(json.dumps({'error': 'Email is required'}), status=400, mimetype='application/json')
    email = data['email']

    try:
        user = Users.query.filter_by(email=email).first()
        if not user:
            return Response(json.dumps({'error': 'User not found'}), status=404, mimetype='application/json')

        promocode_value = get_random_promocode()

        promocode = Promocodes.query.filter_by(value=promocode_value).first()
        promocode.user_email = email
        promocode.created_at = datetime.utcnow()

        user.promocode_id = promocode_value

        send_message(user.email, promocode_value)

        db.session.commit()
        return Response(json.dumps({'promocode': promocode_value}), mimetype='application/json')
    except Exception as e:
        db.session.rollback()
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')


def get_random_promocode():
    promocodes = Promocodes.query.filter_by(user_email=None).all()
    print(len(promocodes))
    promocode = random.choice(promocodes)
    return promocode.value


@app.route('/support', methods=['POST'])
def support_form():
    data = request.get_json();
    if 'email' not in data:
        return Response(json.dumps({'error': 'Email is required'}), status=400, mimetype='application/json')
    if 'text' not in data:
        return Response(json.dumps({'error': 'Message id is required'}), status=400, mimetype='application/json')
    email = data['email']
    text = data['text']
    telegram = data['telegram']
    name = data['name']

    try:
        support_email(email, telegram, name, text)
        return Response(json.dumps({'message': 'Message sent'}), mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')


@app.route('/clear', methods=['GET'])
def clear_users():
    try:
        db.session.query(Users).delete()
        db.session.commit()
        return Response(json.dumps({'message': 'User cleared'}), status=200, mimetype='application/json')
    except Exception as e:
        db.session.rollback()
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')

@app.route('/users', methods=['GET'])
def get_users():
    users = Users.query.all()
    users_list = [OrderedDict([('id', user.id), ('email', user.email), ('user_id', user.user_id), ('promocode_id', user.promocode_id), ('created_at', user.created_at)]) for user in users]
    return Response(json.dumps(users_list, default=str), mimetype='application/json')

@app.route('/use-promocode', methods=['POST'])
def use_promocode():
    data = request.get_json()
    promocode_value = str(data['value'])

    try:
        promocode = Promocodes.query.filter_by(value=promocode_value).first()
        if not promocode:
            return Response(json.dumps({'error': 'Promocode not found'}), status=404, mimetype='application/json')
        if promocode.used == 1:
            return Response(json.dumps({'error': 'Этот промокод уже использован'}), status=409, mimetype='application/json')
        promocode.used = 1
        db.session.commit()
        return Response(json.dumps({'message': f'Промокод {promocode.value} успешно активирован'}), mimetype='application/json')

    except Exception as e:
        # Handle any exceptions and return a 500 error with the exception message
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')





if __name__ == '__main__':
    app.run(port=5001)
    db.create_all()