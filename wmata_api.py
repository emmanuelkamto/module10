import json
import requests
from flask import Flask, Response

# API endpoint URL and access keys
WMATA_API_KEY = "6d50ccd1910d4bb18fa41496f7903462"
INCIDENTS_URL = "https://api.wmata.com/Incidents.svc/json/ElevatorIncidents"
headers = {"api_key": WMATA_API_KEY, 'Accept': '*/*'}

################################################################################

app = Flask(__name__)

# Get incidents by machine type (elevators/escalators)


@app.route("/incidents/<unit_type>", methods=["GET"])
def get_incidents(unit_type):
    # Create an empty list called 'incidents'
    incidents = []

    # Validate unit_type input
    if unit_type.lower() not in ["elevators", "escalators"]:
        return Response(json.dumps({"error": "Invalid unit type"}), status=400, mimetype='application/json')

    # Use 'requests' to do a GET request to the WMATA Incidents API
    response = requests.get(INCIDENTS_URL, headers=headers)

    # Retrieve the JSON from the response
    if response.status_code == 200:
        data = response.json()

        # Define the proper unit type for comparison
        unit_type_comparison = "ELEVATOR" if unit_type.lower() == "elevators" else "ESCALATOR"

        # Iterate through the JSON response and retrieve all incidents matching 'unit_type'
        for incident in data.get("ElevatorIncidents", []):
            if incident.get("UnitType").upper() == unit_type_comparison:
                # Create a dictionary containing the 4 fields from the Module 7 API definition
                incident_dict = {
                    "StationCode": incident.get("StationCode"),
                    "StationName": incident.get("StationName"),
                    "UnitName": incident.get("UnitName"),
                    "UnitType": incident.get("UnitType").upper()
                }
                # Add each incident dictionary object to the 'incidents' list
                incidents.append(incident_dict)

    # Return the list of incident dictionaries using json.dumps()
    return Response(json.dumps(incidents), mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
