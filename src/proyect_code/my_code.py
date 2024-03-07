# Cargando las bibliotecas
from sympy import sympify, to_dnf
from tools.preprocess import Preprocess
from gensim.corpora import Dictionary
import json

# from Models.Boolean_Extended_Model.boolean_extended_model import ExtendedBooleanModel
import ir_datasets
from tools.preprocess_to_query import preprocess_query
from Models.MRI import boolean_MRI


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
            documents.append({"id": doc.doc_id, "title": doc.text})
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


# Uso
cranfield_data = DatasetData()

dictionary = {}
for query_id, doc_id, relevance, iteration in cranfield_data.dataset.qrels_iter():
    if relevance != -1:
        if query_id not in dictionary:
            dictionary[query_id] = [doc_id]
        else:
            dictionary[query_id].append(doc_id)


def relevant_documents(query_id: str):
    """
    Devuelve documentos relevantes dada una consulta y el identificador de la consulta.

    Args:
      - query_id (str) : Identificador de la consulta.

    Return:
      list<str>
    """
    result = dictionary[query_id]
    return result


def recovered_documents_sri(query):
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

    pre_query = preprocess_query(query)
    print(pre_query)
    mri = boolean_MRI(tokenized_docs, pre_query)
    # boolean_extended_model = ExtendedBooleanModel(tokenized_docs, query)
    mri.process_TfidfVectorizer()

    x = mri.similarity_boolean_extended()
    return x


def recovered_documents_sri_standar(query):
    """
    Determina el conjunto de documentos recuperados. El más importante se encuentra en la posición cero y, por lo tanto, la relevancia disminuye.

    Args:
    - query (str): Texto de la consulta.

    Return:
    list: Lista de identificadores de documentos y puntuación.

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

    pre_query = preprocess_query(query)
    print(pre_query)
    mri = boolean_MRI(tokenized_docs, pre_query)
    mri.process_TfidfVectorizer()
    return mri.similarity_boolean_standart()
