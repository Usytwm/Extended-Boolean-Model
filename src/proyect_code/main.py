from flask import Flask, jsonify
import pandas as pd
from datetime import date
from flask_cors import CORS

app = Flask(__name__, template_folder="./templates")
CORS(app)


@app.route("/api/search", methods=["GET"])
def get():
    return jsonify({"error": "Missing query parameter"}), 400


@app.route("/api/all", methods=["GET"])
def get_all():
    return jsonify({"error": "Missing query parameter"}), 400


if __name__ == "__main__":
    app.run(debug=True, port=4000)
