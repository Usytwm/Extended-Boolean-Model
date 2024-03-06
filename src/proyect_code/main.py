from flask import Flask, jsonify
from flask_cors import CORS
import my_code as cd
from tools.metrics import calculate_metrics

app = Flask(__name__, template_folder="./templates")
CORS(app)

metricas_recientes = {"estandar": {}, "extendido": {}}


@app.route("/api/allqueries", methods=["GET"])
def get_all_queries():
    data = cd.cranfield_data.queries
    return jsonify(data)


@app.route("/api/search/<query>", methods=["GET"])
def search_query(query):
    partes = query.split(",")
    query_id = partes[0]
    query = partes[1]
    documents = cd.recovered_documents_sri(query)
    result = list(documents.keys())
    all_documents = cd.cranfield_data.documents
    result1 = [all_documents[key] for key in result[:10]]
    result_values = [doc["id"] for doc in result1]
    # Calcula las métricas después de recuperar los documentos
    truth_values = cd.relevant_documents(query_id)
    metricas_recientes["extendido"] = calculate_metrics(truth_values, result_values)
    return jsonify(result1)


@app.route("/api/searchstandar/<query>", methods=["GET"])
def search_standar_query(query):
    partes = query.split(",")
    query_id = partes[0]
    query = partes[1]
    documents = cd.recovered_documents_sri_standar(query)
    all_documents = cd.cranfield_data.documents
    result1 = [all_documents[key] for key in documents[:10]]
    result_values = [doc["id"] for doc in result1]
    truth_values = cd.relevant_documents(query_id)
    metricas_recientes["estandar"] = calculate_metrics(truth_values, result_values)
    return jsonify(result1)


@app.route("/api/metrics", methods=["GET"])
def get_metrics():
    metric_estandar = metricas_recientes["estandar"]
    metric_extendes = metricas_recientes["extendido"]
    metrics = {
        "data": [
            {
                "name": "Precision",
                "standar": metric_estandar.precision,
                "extended": metric_extendes.precision,
            },
            {
                "name": "r_precision",
                "standar": metric_estandar.r_precision,
                "extended": metric_extendes.r_precision,
            },
            {
                "name": "f1",
                "standar": metric_estandar.f1,
                "extended": metric_extendes.f1,
            },
            {
                "name": "fallout",
                "standar": metric_estandar.fallout,
                "extended": metric_extendes.fallout,
            },
            {
                "name": "recall",
                "standar": metric_estandar.recall,
                "extended": metric_extendes.recall,
            },
        ]
    }
    return jsonify(metrics)


if __name__ == "__main__":
    app.run(debug=True, port=4000)
