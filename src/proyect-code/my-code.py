# Cargando las bibliotecas
import ir_datasets
import nltk
import spacy as sp
import gensim
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from tools.preprocess import Preprocess

# Calcular IDF solo para términos de consulta
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np


# Cargar el diccionario de Gensim
from gensim.corpora import Dictionary


import ir_datasets
import nltk
import spacy as sp
import gensim
from gensim.corpora import Dictionary
import json
from Models.Boolean_Extended_Model.boolean_extended_model import ExtendedBooleanModel

# Intenta cargar documentos preprocesados y el diccionario
try:
    with open("src/proyect-code/Data/preprocessed_docs.json", "r") as f:
        tokenized_docs = json.load(f)
        # Reconstruir los documentos a partir de las listas de palabras
    dictionary = Dictionary.load("src/proyect-code/Data/dictionary.gensim")
except FileNotFoundError:
    dataset = ir_datasets.load("cranfield")
    documents = [doc.text for doc in dataset.docs_iter()]
    preprocess = Preprocess()
    tokenized_docs, dictionary, vocabulary, vector_repr, pos_tags = (
        preprocess.preprocess_documents(documents)
    )
    with open("src/proyect-code/Data/preprocessed_docs.json", "w") as f:
        json.dump(tokenized_docs, f)

    dictionary.save("src/proyect-code/Data/dictionary.gensim")

terminos_consulta = ["experiment", "concept", "physical", "theory"]

boolean_extended_model = ExtendedBooleanModel(tokenized_docs, terminos_consulta)
boolean_extended_model.process()

value = 1393

# Calcular la similitud OR y AND para el primer documento, como ejemplo
doc_weights = boolean_extended_model.get_document_weights(
    value
)  # Obtener los pesos del primer documento
sim_or_value = boolean_extended_model.sim_or(doc_weights)
sim_and_value = boolean_extended_model.sim_and(doc_weights)

print(f"Similitud OR para el Documento {value}: {sim_or_value}")
print(f"Similitud AND para el Documento {value}: {sim_and_value}")
