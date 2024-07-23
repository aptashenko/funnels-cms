from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
from collections import OrderedDict
from mailgun.send_email import send_message
from mailgun.send_support import support_email
import json
import random

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), nullable=False)
    promocode = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/add-user', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data or 'email' not in data:
        return Response(json.dumps({'error': 'Email is required'}), status=400, mimetype='application/json')
    if 'user_id' not in data:
        return Response(json.dumps({'error': 'User id is required'}), status=400, mimetype='application/json')
    email = data['email']
    user_id = data['user_id']
    user = User(email=email, user_id=user_id)

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
        user = User.query.filter_by(email=email).first()
        if not user:
            return Response(json.dumps({'error': 'User not found'}), status=404, mimetype='application/json')

        promocode_value = get_random_promocode();
        user.promocode = promocode_value;
        send_message(user.email, promocode_value);
        db.session.commit()
        return Response(json.dumps({'promocode': promocode_value}), mimetype='application/json')
    except Exception as e:
        db.session.rollback()
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')

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
        db.session.query(User).delete()
        db.session.commit()
        return Response(json.dumps({'message': 'User cleared'}), status=200, mimetype='application/json')
    except Exception as e:
        db.session.rollback()
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [OrderedDict([('id', user.id), ('email', user.email), ('user_id', user.user_id), ('promocode', user.promocode), ('created_at', user.created_at)]) for user in users]
    return Response(json.dumps(users_list, default=str), mimetype='application/json')

def get_random_promocode():
    with open('promocodes.json', 'r') as file:
        promocodes = json.load(file)

        if promocodes:
            promocode = random.choice(promocodes)
            promocodes.remove(promocode)

            with open('promocodes.json', 'w') as file:
                json.dump(promocodes, file)

            return promocode
        else:
            return None

if __name__ == '__main__':
    app.run(port=5001)