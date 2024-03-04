import gensim
import spacy
from sympy import sympify, to_dnf, Not, And, Or

def similarity(query_dnf,tokenized_docs):
  

  # Convertir tokenized_docs a un conjunto de sets
  doc_term_sets = [set(doc) for doc in tokenized_docs]

  matching_documents = []
  for doc_i, doc_terms in enumerate(doc_term_sets):
    # Short-circuiting: si no hay coincidencia con una componente conjuntiva, se ignora el documento
    all_match = True
    for q_ce in query_dnf:
      if not q_ce.issubset(doc_terms):
        all_match = False
        break
    if all_match:
      matching_documents.append(doc_i)

  return matching_documents

