from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

@app.route("/get-distance", methods=["GET"])
def get_distance():
    origin = request.args.get("from")
    destination = request.args.get("to")

    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&key={GOOGLE_API_KEY}"

    response = requests.get(url)
    data = response.json()

    try:
        element = data["rows"][0]["elements"][0]
        distance_text = element["distance"]["text"]
        duration_text = element["duration"]["text"]

        return jsonify({
            "origin": origin,
            "destination": destination,
            "distance": distance_text,
            "duration": duration_text
        })
    except:
        return jsonify({"error": "Invalid location or API response"}), 400

if __name__ == "__main__":
    app.run(debug=True)