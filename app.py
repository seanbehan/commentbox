from flask import Flask, jsonify, request, render_template, json
from lib import search_places, save_comment
from flask_request_params import bind_request_params

app = Flask(__name__)
app.before_request(bind_request_params)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/places.json")
def places():
    lat = float(request.args.get('lat', '0.0'))
    lng = float(request.args.get('lng', '0.0'))

    return json.dumps(search_places(lat=lat,lng=lng))

@app.route("/places/<place_id>.json")
def place(place_id):
    return jsonify(search_places(place_id=place_id))

@app.route("/places/<place_id>/comments.json", methods=["POST"])
def place_comment(place_id):
    comment_params = dict(request.params['comment'])
    comment_params['place_id'] = place_id

    comment = save_comment(comment_params)

    return jsonify(comment)

if __name__ == "__main__":
    app.run(debug=True)
