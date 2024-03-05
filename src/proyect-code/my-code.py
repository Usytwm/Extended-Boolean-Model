# Cargando las bibliotecas
import ir_datasets
from tools.preprocess import Preprocess
from gensim.corpora import Dictionary
import json
from Models.Boolean_Extended_Model.boolean_extended_model import ExtendedBooleanModel

dataset = ir_datasets.load("cranfield")
terminos_consulta = "vegetarian animal culito"
dictionary = {}
for query_id, doc_id, relevance, iteration in dataset.qrels_iter():
    if query_id not in dictionary:
        dictionary[query_id] = [doc_id]
    else:
        dictionary[query_id].append(doc_id)

# for query_id, doc_ids in dictionary.items():
#     if len(doc_ids) > 2:
#         print(query_id)
# print(dictionary)


def relevant_documents(query_id: str):
    """
    Returns relevant documents given a query and the query

    Args:
      - query_id (str) : Query identifier.

    Return:
      list<str>

    """
    for queryt_id, query_text in dataset.queries_iter():
        if queryt_id == query_id:
            break

    return (
        [
            doc_id
            for (queryt_id, doc_id, relevance, iteration) in dataset.qrels_iter()
            if queryt_id == query_id
        ],
        query_text,
    )


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
        with open("src/proyect-code/Data/preprocessed_docs.json", "r") as f:
            tokenized_docs = json.load(f)
            # Reconstruir los documentos a partir de las listas de palabras
        dictionary = Dictionary.load("src/proyect-code/Data/dictionary.gensim")
    except FileNotFoundError:

        documents = [doc.text for doc in dataset.docs_iter()]
        preprocess = Preprocess()
        tokenized_docs, dictionary, vocabulary, vector_repr, pos_tags = (
            preprocess.preprocess_documents(documents)
        )
        with open("src/proyect-code/Data/preprocessed_docs.json", "w") as f:
            json.dump(tokenized_docs, f)

        dictionary.save("src/proyect-code/Data/dictionary.gensim")

    boolean_extended_model = ExtendedBooleanModel(tokenized_docs, query)
    boolean_extended_model.process()
    relevance_scores = boolean_extended_model.all_documents_relevance_and()

    return enumerate(relevance_scores)


print(recovered_documents_sri(terminos_consulta))
