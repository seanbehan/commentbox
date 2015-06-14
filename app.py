from flask import Flask, jsonify, request, render_template, json
from lib import search_places

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome"

@app.route("/places.json")
def places():
    lat = float(request.args.get('lat'))
    lng = float(request.args.get('lng'))

    return json.dumps(search_places(lat=lat,lng=lng))

@app.route("/places/<place_id>.json")
def place(place_id):
    return json.dumps(search_places(place_id=place_id))

@app.route("/places/<place_id>/comments.json")
def place_comment(place_id):
    comment = request.data.get('comment')

    if comment:
        db['comments'].insert(comment)

    return jsonify(search_places(place_id=place_id))

if __name__ == "__main__":
    app.run(debug=True)
