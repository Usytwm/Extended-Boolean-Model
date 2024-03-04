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

def get_literals_from_dnf(dnf):
    literals = []
    for disjunct in dnf.args:
        if not isinstance(disjunct, sympy.logic.boolalg.And):
            literals.append(str(disjunct.as_independent(*disjunct.free_symbols)[1]))
        else:
            for literal in disjunct.args:
                # Convertir cada literal a string
                literals.append(str(literal.as_independent(*disjunct.free_symbols)[1]))
    print(literals)
    
    return literals


    

consulta = "Ant AND (B OR NOT C)"
print('query: ', consulta)
consulta_dnf = query_to_dnf(consulta)
print('dnf expression: ', consulta_dnf)
print('\n')

consulta = "A (B OR NOT C)"
print('query: ', consulta)
consulta_dnf = query_to_dnf(consulta)
print('dnf expression: ', consulta_dnf)
print('\n')

consulta = "A and  C and B and NOT Not C"
print('query: ', consulta)
consulta_dnf = query_to_dnf(consulta)
print('dnf expression: ', consulta_dnf)
print('\n')

consulta = "A C and B and NOT Not C"
print('query: ', consulta)
consulta_dnf = query_to_dnf(consulta)
print('dnf expression: ', consulta_dnf)
print('\n')

consulta = "A C B and NOT Not C"
print('query: ', consulta)
consulta_dnf = query_to_dnf(consulta)
print('dnf expression: ', consulta_dnf)
print('\n')

consulta = "A (C and NOT Not C)"
print('query: ', consulta)
consulta_dnf = query_to_dnf(consulta)
print('dnf expression: ', consulta_dnf)
print('\n')

consulta = "A (C (NOT Not b))"
print('query: ', consulta)
consulta_dnf = query_to_dnf(consulta)
print('dnf expression: ', consulta_dnf)
print('\n')

consulta = "A B OR NOT C)"
print('query: ', consulta)
consulta_dnf = query_to_dnf(consulta)
print('dnf expression: ', consulta_dnf)
print('\n')

consulta = "A B 'OR NOT C)"
print('query: ', consulta)
consulta_dnf = query_to_dnf(consulta)
print('dnf expression: ', consulta_dnf)
print('\n')

consulta = "A AND OR B 'OR NOT Not C)"
print('query: ', consulta)
consulta_dnf = query_to_dnf(consulta)
print('dnf expression: ', consulta_dnf)
# print('\n')