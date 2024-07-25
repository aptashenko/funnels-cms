from flask import Response, request
import json
from app.routes.index import app
from selzy.send_support import support_email
@app.route('/support', methods=['POST'])
def support_form():
    data = request.get_json()
    if 'email' not in data or 'text' not in data:
        return Response(json.dumps({'error': 'Email and text are required'}), status=400, mimetype='application/json')
    email = data['email']
    text = data['text']
    telegram = data.get('telegram')
    name = data.get('name')

    try:
        support_email(email, telegram, name, text)
        return Response(json.dumps({'message': 'Message sent'}), mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')
