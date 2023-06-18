from flask import Flask, jsonify, request

app = Flask(__name__)

AUTH_TOKEN = "token"

data = {
    "favouriteCoffee": "espresso",
    "top3": ["espresso", "cappuccino", "latte"]
}

@app.route('/favourite_drink', methods=['GET'])
def get_favourite_drink():
    token = request.headers.get('Authorization')
    if not token or token != AUTH_TOKEN:
        return jsonify({"message": "Unauthorized"}), 401

    return jsonify({"data": {"favouriteCofee": data["favouriteCoffee"]}})

@app.route('/favourite_drink', methods=['POST'])
def post_favourite_drink():
    token = request.headers.get('Authorization')
    if not token or token != AUTH_TOKEN:
        return jsonify({"message": "Unauthorized"}), 401

    request_data = request.get_json()
    data["top3"] = request_data.get("data", {}).get("top3", data["top3"])
    
    return jsonify({"message": "Data updated successfully"})

@app.route('/favourite_drinks_leaderboard', methods=['GET'])
def get_favourite_drinks_leaderboard():
    token = request.headers.get('Authorization')
    if not token or token != AUTH_TOKEN:
        return jsonify({"message": "Unauthorized"}), 401

    return jsonify({"data": {"top3": data["top3"]}})


if __name__ == '__main__':
    app.run(debug=True)
