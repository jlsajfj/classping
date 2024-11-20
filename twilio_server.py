import os
from twilio.rest import Client

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
from_number = os.environ["FROM_NUMBER"]
client = Client(account_sid, auth_token)


def send_text(message: str, numbers: list[str]) -> None:
    for number in numbers:
        client.messages.create(
            body=message,
            from_=from_number,
            to=number,
        )


numbers = [input("> "), input("> ")]
send_text(input("> "), numbers)
