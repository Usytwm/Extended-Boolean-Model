from flask import Flask, jsonify
from flask_cors import CORS
import my_code as cd


data = cd.DatasetData()

app = Flask(__name__, template_folder="./templates")
CORS(app)


@app.route("/api/allqueries", methods=["GET"])
def get_all_queries():
    data = data.queries
    return jsonify(data)


@app.route("/api/search/<query>", methods=["GET"])
def search_query(query):
    documents = cd.get_documents(query)

    return jsonify(documents)


@app.route("/api/metrics", methods=["GET"])
def get_metrics():
    metrics = {
        "data": [
            {"name": "Page A", "standar": 4000, "extended": 2400},
            {"name": "Page B", "standar": 3000, "extended": 1398},
            # Agrega más objetos según sea necesario
            {"name": "Page C", "standar": 2000, "extended": 9800},
            {"name": "Page D", "standar": 2780, "extended": 3908},
        ]
    }
    return jsonify(metrics)


if __name__ == "__main__":
    app.run(debug=True, port=4000)
