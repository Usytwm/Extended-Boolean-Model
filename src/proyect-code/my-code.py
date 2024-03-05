# Cargando las bibliotecas
import ir_datasets
from sympy import sympify, to_dnf
import sympy
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


# print(recovered_documents_sri(terminos_consulta))
def query_to_dnf(query):

    processed_query = query
    override_and = ("and", "AND", "&&", "&")
    override_or = ("or", "OR", "||", "|")
    override_not = ("not", "NOT", "~")
    override_notp = ("(NOT", "(not", "~")

    processed_query = [token for token in processed_query.split(" ")]

    newFND = " "
    for i, item in enumerate(processed_query):
        if item in override_and:
            processed_query[i] = override_and[-1]
            newFND += " & "
        elif item in override_or:
            processed_query[i] = override_and[-1]
            newFND += " | "
        elif item in override_not:
            processed_query[i] = override_not[-1]
            newFND += "~"
        elif item in override_notp:
            processed_query[i] = override_notp[-1]
            newFND += "(~"

        else:
            newFND += processed_query[i]
            if (
                i < len(processed_query) - 1
                and (not (processed_query[i + 1] in override_and))
                and (not (processed_query[i + 1] in override_or))
                and (not (processed_query[i + 1] in override_not))
            ):
                newFND += " & "

    print("antes ", newFND)
    # Convertir a expresión sympy y aplicar to_dnf
    query_expr = sympify(newFND, evaluate=False)
    query_dnf = to_dnf(query_expr, simplify=True)

    return query_dnf


def get_literals_from_dnf(dnf):
    literals = []
    for disjunct in dnf.args:
        if isinstance(disjunct, sympy.Not):
            literals.append(
                f"~{str(disjunct.args[0])}"
            )  # Include the negation symbol (~)
        else:
            for literal in disjunct.args:
                # Access the literal directly without using 'as_independent'
                literals.append(str(literal))
    return list(set(literals))
