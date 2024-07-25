from flask import Response, request
import json

from models.index import db, Users

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
