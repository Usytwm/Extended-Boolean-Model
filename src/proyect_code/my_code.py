# Cargando las bibliotecas
import ir_datasets
from sympy import sympify, to_dnf
from tools.metrics import calculate_metrics,precision, recall
from tools.preprocess import Preprocess
from tools.prepro import preprocess_documents
from gensim.corpora import Dictionary
from tools.preprocess_to_query import preprocess_query
import json
from Models.MRI import boolean_MRI
import time

dataset = ir_datasets.load("cranfield")
terminos_consulta = "text  what application has the linear theory design of curved wings"

dictionary = {}

for query_id, doc_id, relevance, iteration in dataset.qrels_iter():
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
    #global dataset
    #X = 0
    #for qrel in dataset.qrels_iter():
    #    print("Query_id :", query_id)
    #    if int(qrel[0]) == int(query_id):
    #        print("relevancia :", qrel[3])
    #        X+=1
#
    #
    #print(X)
    return [item[1] for item in dataset.qrels_iter() if (int(item[0]) == int(query_id) and item[2] != -1)]


def recovered_documents_sri(query):
    """
    Determina el conjunto de documentos recuperados. El más importante se encuentra en la posición cero y, por lo tanto, la relevancia disminuye.

    Args:
      - query (str): Texto de la consulta.

    Return:
      list: Lista de identificadores de documentos y puntuación.

    """
    start = time.time()
    # Intenta cargar documentos preprocesados y el diccionario
    try:
        with open("src/proyect_code/Data/preprocessed_docs.json", "r") as f:
            tokenized_docs = json.load(f)
            # Reconstruir los documentos a partir de las listas de palabras
        dictionary = Dictionary.load("src/proyect_code/Data/dictionary.gensim")
    except FileNotFoundError:

        documents = [doc.text for doc in dataset.docs_iter()]
        preprocess = Preprocess()
        tokenized_docs, dictionary, vocabulary, vector_repr, pos_tags = (
            preprocess.preprocess_documents(documents)
        )
        with open("src/proyect_code/Data/preprocessed_docs.json", "w") as f:
            json.dump(tokenized_docs, f)

        dictionary.save("src/proyect_code/Data/dictionary.gensim")

    
    pre_query = preprocess_documents(query, True)
    print(pre_query)
    mri = boolean_MRI(tokenized_docs, pre_query)
    mri.process_TfidfVectorizer()
    return mri.all_documents_relevance_and()


rd = recovered_documents_sri(terminos_consulta)
print("rd")
rr = relevant_documents(53)

print(calculate_metrics(rd,rr))
#print(precision(ra,rr))

#print(calculate_metrics(ra,rr))