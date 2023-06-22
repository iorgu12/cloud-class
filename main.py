from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drinks.db'
db = SQLAlchemy(app)

AUTH_TOKEN = "token"

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    count = db.Column(db.Integer, nullable=False, default=0)


@app.route('/favourite_drink', methods=['GET'])
def get_favourite_drink():
    token = request.headers.get('Authorization')
    if not token or token != AUTH_TOKEN:
        return jsonify({"message": "Unauthorized"}), 401

    favourite_drink = Drink.query.order_by(Drink.count.desc()).first()
    return jsonify({"data": {"favouriteCoffee": favourite_drink.name if favourite_drink else "None"}})


@app.route('/favourite_drink', methods=['POST'])
def post_favourite_drink():
    token = request.headers.get('Authorization')
    if not token or token != AUTH_TOKEN:
        return jsonify({"message": "Unauthorized"}), 401

    request_data = request.get_json()
    drinks = request_data.get("data", {}).get("top3", [])
    
    for drink in drinks:
        db_drink = Drink.query.filter_by(name=drink).first()
        if db_drink:
            db_drink.count += 1
        else:
            new_drink = Drink(name=drink, count=1)
            db.session.add(new_drink)
    
    db.session.commit()

    return jsonify({"message": "Data updated successfully"})


@app.route('/favourite_drinks_leaderboard', methods=['GET'])
def get_favourite_drinks_leaderboard():
    token = request.headers.get('Authorization')
    if not token or token != AUTH_TOKEN:
        return jsonify({"message": "Unauthorized"}), 401

    leaderboard = [drink.name for drink in Drink.query.order_by(Drink.count.desc()).limit(3)]
    return jsonify({"data": {"top3": leaderboard}})


if __name__ == '__main__':
    db.create_all()  # ensure tables are created
    app.run(debug=True, host='0.0.0.0')
