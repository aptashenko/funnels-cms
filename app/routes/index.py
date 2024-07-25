from flask import Flask,request, Response
from app import db

from app.routes.new_user import add_new_user
from app.routes.clear import clear_all_users
from app.routes.send_email import send_email
from selzy.send_support import support_email
from app.routes.users import get_users
from app.routes.use_promocode import use_promocode

import json
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/add-user', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data or 'email' not in data:
        return Response(json.dumps({'error': 'Email is required'}), status=400, mimetype='application/json')
    if 'web_user_id' not in data:
        return Response(json.dumps({'error': 'web_user_id is required'}), status=400, mimetype='application/json')
    email = data['email']
    user_id = data['web_user_id']

    try:
        add_new_user(email, user_id)
        return Response(json.dumps({'message': 'User added successfully'}), mimetype='application/json')
    except Exception as e:
        db.session.rollback()
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')

@app.route('/clear', methods=['GET'])
def clear_all():
    try:
        clear_all_users()
        return Response(json.dumps({'message': 'User cleared'}), status=200, mimetype='application/json')
    except Exception as e:
        db.session.rollback()
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')

@app.route('/send-email', methods=['POST'])
def send_email_to_user():
    data = request.get_json()
    if not data or 'email' not in data:
        return Response(json.dumps({'error': 'Email is required'}), status=400, mimetype='application/json')
    email = data['email']

    try:
        error_message = send_email(email)
        if error_message:
            return Response(json.dumps({'error': error_message}), status=404, mimetype='application/json')
    except Exception as e:
        db.session.rollback()
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')

@app.route('/support', methods=['POST'])
def send_to_support():
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

@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = get_users()
        return Response(json.dumps(users, default=str), mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')

@app.route('/use-promocode', methods=['POST'])
def use_promocode():
    data = request.get_json()
    promocode_value = str(data['value'])

    try:
        message = use_promocode(promocode_value)
        return Response(json.dumps({'message': message.message}), status=message.status, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')
