import json
import requests

MICROSERVICE_URL = "http://localhost:5050/match-score"

# Test 1 - Normal 
print("Test 1 - Correct Format. Everything should result in no errors.")

json_sent = {
    "items": [
        {"id": "Toyota RAV4", "attributes": {"reliability": 9, "fuel_efficiency": 8, "performance": 6}},
        {"id": "Mazda CX-5", "attributes": {"reliability": 8, "fuel_efficiency": 7, "performance": 8}},
        {"id": "Honda CR-V", "attributes": {"reliability": 10, "fuel_efficiency": 9, "performance": 6}}
    ],
    "priorities": {"reliability": 5, "fuel_efficiency": 3, "performance": 1}
}

# Show what we're sending 
print("Sending this json to", MICROSERVICE_URL)
print(json.dumps(json_sent))

# Send it as an http post. json= turns our dictionary into JSON for us
response = requests.post(MICROSERVICE_URL, json=json_sent)

# print Status
print("Status:", response.status_code)
print("Response:", response.text)

if response.status_code == 200:
    print("Match scores, in order of closest first:")
    for result in response.json()["results"]:
        print("  ", result["id"], str(result["match_score"]) + "%")
else:
    print("Failure:", response.json()["error"])

#################

# Test 2 - No priorities

print()
print("Test 2 -- No Priorities")

bad_jason_sent = {"items": json_sent["items"]}

print("Sending this to", MICROSERVICE_URL)
print(json.dumps(bad_jason_sent, indent=2))

response = requests.post(MICROSERVICE_URL, json=bad_jason_sent)

print("Status:", response.status_code)
print("Response:", response.text)

if response.status_code == 200:
    print("Match scores:", response.json()["results"])
else:
    print("Failure:", response.json()["error"])
