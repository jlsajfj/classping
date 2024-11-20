import os
from twilio.rest import Client
from flask import Flask, request, jsonify

app = Flask(__name__)

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


@app.route("/send_sms", methods=["POST"])
def send_sms():
    data = request.json
    course = data.get("course")
    seats_taken = data.get("seats_taken")
    seats_total = data.get("seats_total")
    numbers = data.get("numbers", [])

    if not course or not numbers or seats_taken is None or seats_total is None:
        return (
            jsonify(
                {"error": "Course, numbers, seats_taken, and seats_total are required"}
            ),
            400,
        )

    seats_available = seats_total - seats_taken
    message = f"Opening found!\nCourse: {course}\nSeats Available: {seats_available}\nEnrolled: {seats_taken}/{seats_total}"

    try:
        send_text(message, numbers)
        return jsonify({"success": True, "message": "SMS sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=3333)
