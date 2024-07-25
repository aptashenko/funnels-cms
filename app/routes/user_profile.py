from app.models import Users
def user_profile(web_user_id):
    def user_to_dict(user):
        return {
            'id': user.id,
            'email': user.email,
            'web_user_id': user.web_user_id,
            'promocode_id': user.promocode_id,
            'created_at': user.created_at.isoformat() if user.created_at else None
        }

    user = Users.query.filter_by(web_user_id=web_user_id).first()

    if user:
        return {'status': 200, 'message': user_to_dict(user)}
    else:
        return {'status': 404, 'message': {'web_user_id': None}}