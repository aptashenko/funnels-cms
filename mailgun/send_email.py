import requests

def send_message(to_email):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxec293437b85f4ea5bb82ff52faf4f095.mailgun.org/messages",
        auth=("api", "742b58a4f1ec2980fc8c2da8e5443a6a-8a084751-38c6c65a"),
        data={
            "from": "UTPROZORRO <mailgun@sandboxec293437b85f4ea5bb82ff52faf4f095.mailgun.org>",
            "to": to_email,
            "subject": "Hello",
            "text": "Testing some Mailgun awesomeness!"
        }
    )