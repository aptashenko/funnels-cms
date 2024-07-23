import requests

def support_email(from_email, text):
    url = 'https://api.selzy.com/en/api/sendEmail'
    API_KEY = '6msoo3rk48o6w79wrc6w8s6icm3rkh3zw1eeqida'

    params = {
        'format': 'json',
        'api_key': API_KEY,
        'email': 'aptashenko@utprozorro.com.ua',
        'sender_name': 'UTProzorro',
        'sender_email': from_email,
        'subject': f'Запрос от {from_email}',
        'body': text,
        'list_id': '20625873'
    }

    requests.get(url, params=params)