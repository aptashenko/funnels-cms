import requests
from flask import render_template
from datetime import datetime, timedelta

def send_message(to_email, promocode):
    url = 'https://api.selzy.com/en/api/sendEmail'
    API_KEY = '6msoo3rk48o6w79wrc6w8s6icm3rkh3zw1eeqida'

    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    formatted_date = tomorrow.strftime("%d.%m.%Y")

    params = {
        'format': 'json',
        'api_key': API_KEY,
        'email': to_email,
        'sender_name': 'UTProzorro',
        'sender_email': 'aptashenko@utprozorro.com.ua',
        'subject': 'Ваш промокод чекає на Вас',
        'body': render_template('email.html', promocode=promocode, date=formatted_date),
        'list_id': '20625873'
    }

    requests.get(url, params=params)