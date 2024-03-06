import math
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from sympy import sympify, to_dnf, symbols, And
import sympy


class boolean_MRI:
    def __init__(self, tokenized_docs, query):
        self.tokenized_docs = tokenized_docs
        self.weights = None
        self.tokenized_docs = tokenized_docs
        self.query = query
        self.terms_of_interest = self.process_query(query)
        # self.vectorizer_Tfidf = TfidfVectorizer(vocabulary=self.terms_of_interest)
        self.vectorizer = CountVectorizer(vocabulary=self.terms_of_interest)
        self.transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
        self.query_dnf = self.query_to_dnf(self.query)
        self.terms_of_interest_TfidfVectorizer = self.get_literals_from_dnf(
            self.query_dnf
        )
        self.vectorizer_Tfidf = TfidfVectorizer(vocabulary=self.terms_of_interest)
        self.process_TfidfVectorizer()  # Asegura que self.weights se calcule primero

        self.tf = None
        self.idf = None
        self.max_idf = None
        self.weights = None

    def process_query1(self, query):
        """
        Procesa la consulta para obtener los términos de interés.
        """
        # Separar la consulta en términos usando espacios y eliminar espacios en blanco extra
        terms = query.split()
        return [term.strip() for term in terms if term.strip()]

    def process_query(self, query):
        """
        Procesa la consulta para obtener los términos de interés, eliminando operadores lógicos
        y caracteres especiales como paréntesis.
        """
        # Primero, remover caracteres especiales (paréntesis) que no sean relevantes para la separación de términos
        cleaned_query = query.replace("(", "").replace(")", "")
        # Separar la consulta en términos usando espacios
        terms = cleaned_query.split()
        # Filtrar los términos, eliminando los operadores lógicos (en mayúsculas y minúsculas)
        logical_operators = {"and", "or", "not", "AND", "OR", "NOT"}
        filtered_terms = [term for term in terms if term not in logical_operators]

        return filtered_terms

    def vectorize_documents(self):
        """Vectorize the tokenized documents using CountVectorizer."""
        X = self.vectorizer.fit_transform(self.tokenized_docs)
        self.tf = X.toarray()

    def calculate_idf(self):
        """Calculate IDF using TfidfTransformer."""
        self.transformer.fit(self.tf)
        self.idf = self.transformer.idf_
        self.max_idf = np.max(self.idf)

    def calculate_weights(self):
        """Calculate the weights for terms of interest in each document."""
        indices = [
            self.vectorizer.vocabulary_[term]
            for term in self.terms_of_interest
            if term in self.vectorizer.vocabulary_
        ]
        # self.weights = np.clip(
        #     self.tf[:, indices] * (self.idf[indices] / self.max_idf), 0, 1
        # )
        self.weights = self.tf[:, indices] * (self.idf[indices] / self.max_idf)
        self.weights = normalize(self.weights, norm="l2")

    def sim_or(self, document_weights, p=2):
        """Calculate similarity_boolean_standart using OR operation."""
        return np.power(
            np.sum(np.power(document_weights, p)) / len(document_weights), 1 / p
        )

    def sim_and(self, document_weights, p=2):
        """Calculate similarity_boolean_standart using AND operation."""
        return 1 - np.power(
            np.sum(np.power(1 - document_weights, p)) / len(document_weights), 1 / p
        )

    def all_documents_relevance_or(self, p=2):
        """Calcula la relevancia de todos los documentos usando la operación OR."""
        relevances = [
            self.sim_or(self.get_document_weights(i), p)
            for i in range(len(self.tokenized_docs))
        ]
        return relevances

    def all_documents_relevance_and(self, p=2):
        """Calcula la relevancia de todos los documentos usando la operación AND."""
        relevances = [
            self.sim_and(self.get_document_weights(i), p)
            for i in range(len(self.tokenized_docs))
        ]
        return relevances

    def process(self):
        """Process the documents to calculate the TF-IDF weights."""
        self.vectorize_documents()
        self.calculate_idf()
        self.calculate_weights()

    def get_document_weights(self, doc_index):
        """Get the TF-IDF weights for a specific document."""
        if self.weights is not None:
            return self.weights[doc_index]
        else:
            return None

    def process_TfidfVectorizer(self):
        """
        Vectoriza los documentos tokenizados y calcula los pesos TF-IDF.
        """
        # Convierte la lista de documentos tokenizados en una lista de strings separados por espacios.
        documents = [doc for doc in self.tokenized_docs]
        # Ajusta el vectorizador a los documentos y transforma los documentos en una matriz TF-IDF.
        tfidf_matrix = self.vectorizer_Tfidf.fit_transform(documents)
        # Convierte la matriz TF-IDF sparse a una matriz densa y la almacena en self.weights.
        self.weights = tfidf_matrix.toarray()
        self.feature_names = self.vectorizer_Tfidf.get_feature_names_out()

    def query_to_dnf(self, query):
        processed_query = query
        override_and = ("and", "AND", "&&", "&")
        override_or = ("or", "OR", "||", "|")
        override_not = ("not", "NOT", "~")
        override_notp = ("(NOT", "(not", "~")

        processed_query = [token for token in processed_query.split(" ")]

        newFND = ""
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
        print(newFND)
        try:
            query_expr = sympify(newFND, evaluate=False)
        except:
            simb = symbols(newFND)
            query_expr = And(*simb)
            query_expr = sympify(query_expr, evaluate=False)
        query_dnf = to_dnf(query_expr, simplify=True, force=True)
        return query_dnf

    def get_literals_from_dnf(self, dnf):
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

    def similarity_boolean_standart(self):
        # Convert tokenized_docs to a list of sets for efficient operations
        doc_term_sets = self.tokenized_docs

        matching_documents = []
        for doc_i, doc_terms in enumerate(doc_term_sets):
            # Initialize a flag to check if the document matches the query
            all_match = False
            for q_ce in self.query_dnf.args:
                # Check if the query component is a subset of the document terms
                try:
                    for elem in str(q_ce).split("&"):
                        if elem not in doc_terms:
                            # If any component of the query matches, the document is a match
                            break
                    else:
                        all_match = True
                except:
                    if str(q_ce) in doc_terms:
                        all_match = True
                if all_match:
                    matching_documents.append(doc_i)
                    break

            # If the document matches all components of the query, add it to the list

        return matching_documents

    def similarity_boolean_extended(self):
        """
        Calcula la similitud entre la consulta DNF y los documentos, basándose en los pesos TF-IDF.
        """
        scores = {}
        literals_total = len(self.terms_of_interest)

        for doc_index in range(len(self.tokenized_docs)):
            _or = 0
            _or_count = 0
            for clause in self.query_dnf.args:
                _or_count += 1
                if not isinstance(clause, sympy.And):
                    term = (
                        clause if isinstance(clause, sympy.Symbol) else clause.args[0]
                    )
                    term_str = str(term)
                    if term_str in self.feature_names:
                        term_index = np.where(self.feature_names == term_str)[0][0]
                        tfxidf_term = self.weights[doc_index][term_index]
                        _or += (
                            math.pow(tfxidf_term, literals_total)
                            if not isinstance(clause, sympy.Not)
                            else -math.pow(tfxidf_term, literals_total)
                        )
                else:
                    _and = 0
                    _and_count = 0
                    for literal in clause.args:
                        _and_count += 1
                        term = (
                            literal
                            if isinstance(literal, sympy.Symbol)
                            else literal.args[0]
                        )
                        term_str = str(term)
                        if term_str in self.feature_names:
                            term_index = np.where(self.feature_names == term_str)[0][0]
                            tfxidf_term = self.weights[doc_index][term_index]
                            _and += (
                                math.pow(1 - tfxidf_term, literals_total)
                                if not isinstance(literal, sympy.Not)
                                else -(1 - math.pow(tfxidf_term, literals_total))
                            )

                    if _and_count > 0:
                        _or += math.pow(
                            1 - math.pow(_and / _and_count, 1 / literals_total),
                            literals_total,
                        )

            if _or_count > 0:
                scores[doc_index] = math.pow(_or / _or_count, 1 / literals_total)

        scores = {
            doc: score
            for doc, score in sorted(
                scores.items(), key=lambda item: item[1], reverse=True
            )
            if score > 0
        }

        return scores

    def get_document_weights_TfidfVectorizer(self, doc_index):
        """
        Obtiene los pesos TF-IDF para un documento específico.
        """
        if self.weights is not None:
            return self.weights[doc_index]
        else:
            return None
