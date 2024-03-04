import math
from query_preppro import query_to_dnf
from ...data.code.process import corpus
import sympy


_corpus = corpus('cranfield', 10)

feature_names = ''
extended_matrix = ''

def similarity(query_list, query_dnf):

    literals_total = len(query_list)
     
    scores = dict()
    
    for doc in _corpus.docs:
        _or = 0
        _or_count = 0
        for clause in query_dnf.args:
            _or_count += 1
            if not isinstance(clause, sympy.logic.boolalg.And):
                # Obtener el termino
                term = clause.as_independent(*clause.free_symbols)[1]
                # Obtener el indice del termino en la matriz
                term_index = feature_names.index(term)
                
                # Ver el valor de la matriz en la posicion doc, term
                tfxidf_term = extended_matrix[doc.index, term_index]
                
                # Annadir el valor de ese termino en dependencia de si es un not o no
                _or += math.pow(tfxidf_term, literals_total) if not isinstance(clause, sympy.logic.boolalg.Not) else - math.pow(tfxidf_term, literals_total)
            else:
                _and = 0
                _and_count = 0
                for literal in clause.args:  
                    _and_count += 1  
                    # Obtener el termino
                    term = literal.as_independent(*literal.free_symbols)[1]
                    # Obtener el indice del termino en la matriz
                    term_index = feature_names.index(term)

                    # Ver el valor de la matriz en la posicion doc, term
                    tfxidf_term = extended_matrix[doc.index, term_index]
                    
                    _and += math.pow(1 - tfxidf_term, literals_total) if not isinstance(clause, sympy.logic.boolalg.Not) else - (1 - math.pow(tfxidf_term, literals_total))
               
                # Calculo la raiz p-esima 
                _or += math.pow(1 - math.sqrt(_and/_and_count, 1/literals_total), literals_total)
        
        scores.update(doc.index, math.pow(_or / _or_count, literals_total))
    scores = dict(sorted(scores.items(), key=lambda item: item[1]))
    print([doc[0] for doc in scores.items])
    return ([doc[0] for doc in scores.items])

