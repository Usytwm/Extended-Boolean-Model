# Cargando las bibliotecas
from sympy import sympify, to_dnf
import sympy
from tools.preprocess import Preprocess
from gensim.corpora import Dictionary
import json
from Models.Boolean_Extended_Model.boolean_extended_model import ExtendedBooleanModel
import ir_datasets


class DatasetData:
    def __init__(self, name="cranfield"):
        self.dataset = ir_datasets.load(name)
        self.documents = self.load_documents()
        self.queries = self.load_queries()
        self.query_responses = self.load_query_responses()

    def load_documents(self):
        """Carga todos los documentos en una lista."""
        documents = []
        for doc in self.dataset.docs_iter():
            documents.append({"id": doc.doc_id, "text": doc.text})
        return documents

    def load_queries(self):
        """Carga todas las consultas en una lista."""
        queries = []
        for query in self.dataset.queries_iter():
            queries.append({"id": int(query.query_id), "name": query.text})
        return queries

    def load_query_responses(self):
        """Carga las respuestas para cada consulta en un diccionario."""
        query_responses = {}
        for qrel in self.dataset.qrels_iter():
            query_id = qrel.query_id
            doc_id = qrel.doc_id
            # Puedes decidir incluir más información de qrel, como el grado de relevancia
            if query_id not in query_responses:
                query_responses[query_id] = [doc_id]
            else:
                query_responses[query_id].append(doc_id)
        return query_responses


# # Uso
# cranfield_data = DatasetData()

# terminos_consulta = "experimental and (equation or culito)"
# dictionary = {}
# for query_id, doc_id, relevance, iteration in cranfield_data.dataset.qrels_iter():
#     if query_id not in dictionary:
#         dictionary[query_id] = [doc_id]
#     else:
#         dictionary[query_id].append(doc_id)


# # Para ver los documentos
# print("Documentos:", cranfield_data.documents[:5])  # Imprime los primeros 5 documentos

# # Para ver las consultas
# print("Consultas:", cranfield_data.queries[:5])  # Imprime las primeras 5 consultas

# # Para ver las respuestas de una consulta específica
# consulta_especifica_id = (
#     "1"  # Asegúrate de usar un ID de consulta válido que exista en el dataset
# )
# print("Respuestas para la consulta:", cranfield_data.load_query_responses)


def recovered_documents_sri(query, datasets):
    """
    Determines the set of documents recovered. The most important one is in position zero and thus the relevance decreases.

    Args:
      - query (str): Query text.

    Return:
      list: List of document identifiers and score

    """
    # Intenta cargar documentos preprocesados y el diccionario
    try:
        with open("src/proyect_code/Data/preprocessed_docs.json", "r") as f:
            tokenized_docs = json.load(f)
            # Reconstruir los documentos a partir de las listas de palabras
        dictionary = Dictionary.load("src/proyect_code/Data/dictionary.gensim")
    except FileNotFoundError:

        documents = [doc.text for doc in cranfield_data.dataset.docs_iter()]
        preprocess = Preprocess()
        tokenized_docs, dictionary, vocabulary, vector_repr, pos_tags = (
            preprocess.preprocess_documents(documents)
        )
        with open("src/proyect_code/Data/preprocessed_docs.json", "w") as f:
            json.dump(tokenized_docs, f)

        dictionary.save("src/proyect_code/Data/dictionary.gensim")

    boolean_extended_model = ExtendedBooleanModel(tokenized_docs, query)
    boolean_extended_model.process_TfidfVectorizer()

    x = boolean_extended_model.sim()
    return x


def get_queries(dataset):
    # Lista para almacenar las consultas
    queries = []

    # Iterar sobre cada consulta en el dataset
    for query in dataset.queries_iter():
        # Cada objeto query generalmente tiene un 'query_id' y un 'text'
        # La estructura exacta puede variar dependiendo del dataset
        query_dict = {"id": int(query.query_id), "name": query.text}
        queries.append(query_dict)

    return queries


def get_documents(query: str):
    """
    Returns relevant documents given a query and the query

    Args:
    - query_id (str) : Query identifier.

    Return:
    list<str>

    """
    return recovered_documents_sri(query)
