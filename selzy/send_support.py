import requests
from flask import render_template
def support_email(from_email, telegram, name, message):
    url = 'https://api.selzy.com/en/api/sendEmail'
    API_KEY = '6msoo3rk48o6w79wrc6w8s6icm3rkh3zw1eeqida'

    params = {
        'format': 'json',
        'api_key': API_KEY,
        'email': 'aptashenko@utprozorro.com.ua',
        'sender_name': 'UTProzorro',
        'sender_email': 'aptashenko@utprozorro.com.ua',
        'subject': f'Запрос от {from_email}',
        'body': render_template('support.html', email=from_email, name=name, telegram=telegram, message=message),
        'list_id': '20625873'
    }

    print(params)

    requests.get(url, params=params)