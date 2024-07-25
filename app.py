from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask import Flask, request, Response
from app.routes.add_user import add_new_user
from app.routes.clear import clear_all_users
from app.routes.send_email import send_email
from selzy.send_support import support_email
from app.routes.users import get_users
from app.routes.use_promocode import use_promocode
from app.services import reset_expired_promocodes
from app.routes.user_profile import user_profile
import json

app = Flask(__name__)
CORS(app)

MYSQL_HOST = 'ovh6.mirohost.net'
MYSQL_USER = 'u_aptashenko'
MYSQL_PASSWORD = 'Aptashenko93'
MYSQL_DB = 'utprozorro_db'

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# reset_expired_promocodes(db)


@app.route('/')
def index():
    return 'Hello World!'

@app.route('/profile')
def get_users_profile():
    web_user_id = request.headers.get('Authorization')
    if 'web_user_id' == None:
        return Response(json.dumps({'error': 'web_user_id is required'}), status=400)

    try:
        response = user_profile(web_user_id)
        return Response(json.dumps(response['message']), status=response['status'], mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500)

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
        response = send_email(email)
        return Response(json.dumps(response['message']), status=response['status'], mimetype='application/json')

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
        return Response(json.dumps(message['message']), status=message['status'], mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')

if __name__ == '__main__':
    app.run(port=5001)
    db.create_all()