import gensim
import spacy
from sympy import sympify, to_dnf, Not, And, Or

def query_to_dnf(query):
    processed_query = "A AND (B OR NOT C)"
    override_and = ('and','AND','&&','&')
    override_or = ('or','OR','||', '|')
    override_not = ('not','NOT','~')

    processed_query = [token for token in processed_query.split(' ')]
    newFND = " "
    for (i, item) in enumerate(processed_query):
        if item in override_and:
            processed_query[i] = override_and[-1]
            newFND += " &"
        elif item in override_or:
            processed_query[i] = override_and[-1]
            newFND += " |"
        elif item in override_not:
            processed_query[i] = override_not[-1]
            newFND += " ~"
        
        else:
            newFND+= " " + processed_query[i]
        if i < len(processed_query)-1 and (not processed_query[i+1] in override_and) and (not processed_query[i+1] in override_or) and (not processed_query[i+1] in override_not) and not "(":
            newFND+=" &"  
    return newFND

    # Convertir a expresión sympy y aplicar to_dnf
    query_expr = sympify(processed_query, evaluate=False)
    query_dnf = to_dnf(query_expr, simplify=True)

    return query_dnf

def get_matching_docs(query_dnf,tokenized_docs):
  

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

