from flask import Flask, request, jsonify
app = Flask(__name__)


# type validation 
def is_number(value):
    if type(value) == int or type(value) == float:
        return True 


# Checks the request for a valid json
def check_request(data):
    if data is None:
        return "Send JSON with items and priorities value"
    if "items" not in data:
        return "Missing items field in json"
    if "priorities" not in data:
        return "Missing priorities field in json"
    if len(data["priorities"]) == 0:
        return "priorities must have at least 1 priority"
    return ""


# Works out how well one car matches as a percent from 0 to 100%
def calculate_score(attributes, priorities):
    points = 0          # the points this car gets
    perfect_points = 0  # the denominator, represents 100% after adjustment

    for name in priorities:
        weight = priorities[name]          # weight of a rating from 1-5
        rating = attributes.get(name, 0)   # the car's score in the category from 0-10

        #formula here
        points = points + weight * rating
        perfect_points = perfect_points + weight * 10
    percent = points / perfect_points * 100
    return round(percent)


# Used for sorting. Tells sort() to put results in order
def get_score(result):
    return result["match_score"]

##########

# Sending the post request 
@app.route("/match-score", methods=["POST"])
def match_score():
    # step 1 -- read json that was sent
    data = request.get_json(silent=True)
    print("Received a request:", data)

    # step 2 -- check if format is correct
    error = check_request(data)
    if error != "":
        print("Sending back an error:", error)
        return jsonify({"error": error}), 400

    # step 3 -- Calcuate each car's score
    results = []
    for item in data["items"]:
        score = calculate_score(item["attributes"], data["priorities"])
        results.append({"id": item["id"], "match_score": score})

    # step 4 -- Put the closest match first
    results.sort(key=get_score, reverse=True)

    # step 5 -- send the results back (status 200 means it worked)
    print("Sending back:", results)
    return jsonify({"results": results}), 200

# microservice is on port 5050
app.run(port=5050)
