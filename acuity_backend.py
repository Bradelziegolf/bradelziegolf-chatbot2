from flask import Flask, request, jsonify
import requests
import os
from base64 import b64encode

from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://bradelziegolf.com"])



# --- Secure Config ---
# Store these in an .env file, NOT directly in code
ACUITY_USER_ID = os.getenv("ACUITY_USER_ID", "18587901")
ACUITY_API_KEY = os.getenv("ACUITY_API_KEY")  # put your key in .env file

# Build authorization header
def auth_header():
    token = b64encode(f"{ACUITY_USER_ID}:{ACUITY_API_KEY}".encode()).decode()
    return {"Authorization": f"Basic {token}"}

# --- ROUTES ---

@app.route("/availability")
def get_availability():
    """
    Returns available times for the chosen appointment type
    for the next 14 days.
    """
    import datetime, os, requests
    from flask import jsonify

    try:
        user_id = os.getenv("ACUITY_USER_ID")
        api_key = os.getenv("ACUITY_API_KEY")
        appointment_type_id = 79560191

        today = datetime.date.today()
        end_date = today + datetime.timedelta(days=14)

        url = (
            f"https://acuityscheduling.com/api/v1/availability/times?"
            f"appointmentTypeID={appointment_type_id}"
            f"&start_date={today.isoformat()}&end_date={end_date.isoformat()}"
        )

        response = requests.get(url, auth=(user_id, api_key))
        data = response.json()

        # Flatten the structure to simple list of time dicts
        times = []
        if isinstance(data, list):
            for day in data:
                if "time" in day:
                    times.append({"time": day["time"]})
                elif "times" in day:
                    for t in day["times"]:
                        times.append({"time": t["time"]})

        return jsonify(times)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/book", methods=["POST"])
def book_appointment():
    """
    Create a new appointment booking.
    Required JSON fields: appointmentTypeID, datetime, firstName, lastName, email
    """
    data = request.json
    acuity_url = "https://acuityscheduling.com/api/v1/appointments"
    response = requests.post(acuity_url, headers={**auth_header(), "Content-Type": "application/json"}, json=data)
    return jsonify(response.json())

@app.route("/")
def home():
    return jsonify({"message": "Brad Elzie Golf API running successfully."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
