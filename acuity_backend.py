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

@app.route("/availability", methods=["GET"])
def get_availability():
    """
    Fetch available times from Acuity Scheduling.
    Optional query params: appointmentTypeID, month, day, calendarID, etc.
    Docs: https://developers.acuityscheduling.com/reference/availabilitytimes
    """
    appointment_type_id = request.args.get("appointmentTypeID") or ""
    params = {}
    if appointment_type_id:
        params["appointmentTypeID"] = appointment_type_id

    acuity_url = "https://acuityscheduling.com/api/v1/availability/times"
    response = requests.get(acuity_url, headers=auth_header(), params=params)
    return jsonify(response.json())

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
