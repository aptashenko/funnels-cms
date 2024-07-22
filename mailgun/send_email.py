import requests
from flask import render_template

def send_message(to_email, promocode):
    url = 'https://api.selzy.com/en/api/sendEmail'
    API_KEY = '6msoo3rk48o6w79wrc6w8s6icm3rkh3zw1eeqida'

    params = {
        'format': 'json',
        'api_key': API_KEY,
        'email': to_email,
        'sender_name': 'UTProzorro',
        'sender_email': 'aptashenko2019@gmail.com',
        'subject': 'Ваша промокод здесь!',
        'body': render_template('email.html', promocode=promocode),
        'list_id': '20625873'
    }

    requests.get(url, params=params)