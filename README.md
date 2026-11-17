Overview
--------

The Match Score microservice tells you how well each item matches what a user cares about.

We are sending 2 things

- items: the things to compare (in this case, cars). Each item has a name (id) and ratings from 0 - 10.
- priorities: what the user cares about. Each one has a weight from 1 (cares a little) to 5 (cares a lot).

It sends back a match score from 0 to 100% for each item

How to run 
----------

Start the microservice by running this in terminal

python3 match_score_service.py


Communication Contract
----------------------

The microservice is a REST API. Programs talk to it by sending http requests with json. 

How to request data
-------------------

Send an http post request to http://localhost:5050/match-score

The body must be a JSON with these two fields comppleted in the correct format

- items (a list): the things to score. Each item needs an "id" (its name) and "attributes" (its ratings, each a number from 0 - 10).
- priorities (an object): what the user cares about. Each value is a weight from 1 to 5. Minimum of 1.


Example
--------

    import requests

    MICROSERVICE_URL = "http://localhost:5050/match-score"

    json_sent = {
        "items": [
            {"id": "Toyota RAV4", "attributes": {"reliability": 9, "fuel_efficiency": 8, "performance": 6}},
            {"id": "Mazda CX-5", "attributes": {"reliability": 8, "fuel_efficiency": 7, "performance": 8}}
        ],
        "priorities": {"reliability": 5, "fuel_efficiency": 3, "performance": 1}
    }

    response = requests.post(MICROSERVICE_URL, json=json_sent)

How to recieve data
-------------------

The microservice replies with JSON and a status code.

Status 200 means everything is correct. "results" lists each item's id and % match. Sorted from best to worst:

{"results": [{"id": "Toyota RAV4", "match_score": 83}, {"id": "Mazda CX-5", "match_score": 77}]}

Status 400 means something is wrong with the request. Followed by explaination.

{"error": "Missing priorities field in json"}

Example
-------

    if response.status_code == 200:
        for result in response.json()["results"]:
            print(result["id"], str(result["match_score"]) + "%")
    else:
        print("Failure:", response.json()["error"])

Score formula
-------------

match_score = (sum of weight x rating) / (sum of weight x 10) x 100


UML Sequence Diagram is included in the video 

