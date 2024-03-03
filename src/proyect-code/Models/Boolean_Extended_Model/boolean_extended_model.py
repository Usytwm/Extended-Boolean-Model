import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize


class ExtendedBooleanModel:
    def __init__(self, tokenized_docs, query):
        self.tokenized_docs = tokenized_docs
        self.weights = None
        self.tokenized_docs = tokenized_docs
        self.query = query
        self.terms_of_interest = self.process_query(query)
        self.vectorizer1 = TfidfVectorizer(vocabulary=self.terms_of_interest)
        self.vectorizer = CountVectorizer(vocabulary=self.terms_of_interest)
        self.transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
        self.tf = None
        self.idf = None
        self.max_idf = None
        self.weights = None

    def process_query(self, query):
        """
        Procesa la consulta para obtener los términos de interés.
        """
        # Separar la consulta en términos usando espacios y eliminar espacios en blanco extra
        terms = query.split()
        return [term.strip() for term in terms if term.strip()]

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
        """Calculate similarity using OR operation."""
        return np.power(
            np.sum(np.power(document_weights, p)) / len(document_weights), 1 / p
        )

    def sim_and(self, document_weights, p=2):
        """Calculate similarity using AND operation."""
        return 1 - np.power(
            np.sum(np.power(1 - document_weights, p)) / len(document_weights), 1 / p
        )

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
        tfidf_matrix = self.vectorizer1.fit_transform(documents)
        # Convierte la matriz TF-IDF sparse a una matriz densa y la almacena en self.weights.
        self.weights = tfidf_matrix.toarray()

    def get_document_weights_TfidfVectorizer(self, doc_index):
        """
        Obtiene los pesos TF-IDF para un documento específico.
        """
        if self.weights is not None:
            return self.weights[doc_index]
        else:
            return None
