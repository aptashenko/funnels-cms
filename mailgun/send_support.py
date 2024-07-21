import requests

def support_email(from_email, text):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxec293437b85f4ea5bb82ff52faf4f095.mailgun.org/messages",
        auth=("api", "742b58a4f1ec2980fc8c2da8e5443a6a-8a084751-38c6c65a"),
        data={
            "from": from_email,
            "to": "aptashenko2019@gmail.com",
            "subject": f'SUPPORT REQUEST, USER {from_email}',
            "text": text
        }
    )