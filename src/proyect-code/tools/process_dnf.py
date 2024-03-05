import gensim
import spacy
from sympy import sympify, to_dnf, Not, And, Or
import sympy
import preprocess

def query_to_dnf(query):

    processed_query = query
    override_and = ('and','AND','&&','&')
    override_or = ('or','OR','||', '|')
    override_not = ('not','NOT','~')
    override_notp = ('(NOT','(not','~')

    processed_query = [token for token in processed_query.split(' ')]
    
    newFND = " "
    for (i, item) in enumerate(processed_query):
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
            newFND+= processed_query[i]
            if i < len(processed_query)-1 and (not (processed_query[i+1] in override_and)) and (not (processed_query[i+1] in override_or)) and (not (processed_query[i+1] in override_not)):
                newFND+=" & "
    
    print("antes ",newFND)
    # Convertir a expresión sympy y aplicar to_dnf
    query_expr = sympify(newFND, evaluate=False)
    query_dnf = to_dnf(query_expr, simplify=True)
    
    return query_dnf


def get_literals_from_dnf(dnf):
    literals = []
    for disjunct in dnf.args:
        if isinstance(disjunct, sympy.Not):
            literals.append(f"~{str(disjunct.args[0])}")  # Include the negation symbol (~)
        else:
            for literal in disjunct.args:
                # Access the literal directly without using 'as_independent'
                literals.append(str(literal))
    return list(set(literals))

consulta = "Ant AND (B OR NOT C)"
print('query: ', consulta)
consulta_dnf = get_literals_from_dnf(query_to_dnf(consulta))
print('dnf expression: ', consulta_dnf)
print('\n')

#consulta = "Ant AND (B OR NOT C)"
#print('query: ', consulta)
#consulta_dnf = query_to_dnf(consulta)
#print('dnf expression: ', consulta_dnf)
#print('\n')
#
consulta = "A (B OR NOT C)"
print('query: ', consulta)
consulta_dnf = get_literals_from_dnf(query_to_dnf(consulta))
print('dnf expression: ', consulta_dnf)
print('\n')
#
#consulta = "A and  C and B and NOT Not C"
#print('query: ', consulta)
#consulta_dnf = query_to_dnf(consulta)
#print('dnf expression: ', consulta_dnf)
#print('\n')
#
#consulta = "A C and B and NOT Not C"
#print('query: ', consulta)
#consulta_dnf = query_to_dnf(consulta)
#print('dnf expression: ', consulta_dnf)
#print('\n')
#
#consulta = "A C B and NOT Not C"
#print('query: ', consulta)
#consulta_dnf = query_to_dnf(consulta)
#print('dnf expression: ', consulta_dnf)
#print('\n')
#
#consulta = "A (C and NOT Not C)"
#print('query: ', consulta)
#consulta_dnf = query_to_dnf(consulta)
#print('dnf expression: ', consulta_dnf)
#print('\n')

#consulta = "A and (C and (Not b))"
#consulta = consulta.lower()
#print('query: ', consulta)
#consulta_dnf = query_to_dnf(consulta)
#print('dnf expression: ', consulta_dnf)
#print('\n')
#
#consulta = "A (C (Not b))"
#print('query: ', consulta)
#consulta_dnf = query_to_dnf(consulta.lower())
#print('dnf expression: ', consulta_dnf)
#print('\n')

#consulta = "A B OR NOT C)"
#print('query: ', consulta)
#consulta_dnf = query_to_dnf(consulta)
#print('dnf expression: ', consulta_dnf)
#print('\n')
#
#consulta = "A B 'OR NOT C)"
#print('query: ', consulta)
#consulta_dnf = query_to_dnf(consulta)
#print('dnf expression: ', consulta_dnf)
#print('\n')
#
#consulta = "A AND OR B 'OR NOT Not C)"
#print('query: ', consulta)
#consulta_dnf = query_to_dnf(consulta)
#print('dnf expression: ', consulta_dnf)
## print('\n')

#
#def get_literals_from_dnf(dnf):
#    #dnf = dnf.split()
#    literals = []
#    for disjunct in dnf.args:
#        if not isinstance(disjunct, sympy.logic.boolalg.And):
#            literals.append(str(disjunct.args[0]))  # Accede al operando de 'Not'
#        else:
#            for literal in disjunct.args:
#                # Convertir cada literal a string
#                literals.append(str(literal.as_independent(*disjunct.free_symbols)[1]))
#    print(literals)
#    
#    return literals
#
#

#def query_to_dnf(query):
#    query = preprocess.preprocess_documents([query],True)[0]
#    
#    temporal_query = query
#    
#    operators = ['and', 'or', 'not']
#    
#    query = temporal_query[0]
#    
#    for i in range(len(temporal_query) - 1):
#        if (not temporal_query[i] in operators and not temporal_query[i + 1] in operators) \
#                and not (temporal_query[i][0] == '(' and temporal_query[i + 1][-1] == ')'):
#            query += ' and ' + temporal_query[i + 1]
#        else:
#            query += " " + temporal_query[i + 1]
#            
#    processed_query = query.replace('and', '&').replace('&&', '&').replace('or', '|').replace('||', '|').replace('not', '~')
#    print(processed_query)
#    
#    # Convertir a expresión sympy y aplicar to_dnf. Cuando no existe operador entre un literal y un parentesis abiierto Sympy asume que es un AND
#    query_expr = sympify(processed_query, evaluate=False)
#    # print('logical expression: ', query_expr)
#    query_dnf = to_dnf(query_expr, simplify=True)
#    
#    
#    return query_dnf
