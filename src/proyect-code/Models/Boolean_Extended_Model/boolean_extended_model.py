import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


class ExtendedBooleanModel:
    def __init__(self, tokenized_docs, terms_of_interest):
        self.tokenized_docs = tokenized_docs
        self.terms_of_interest = terms_of_interest
        self.vectorizer = CountVectorizer(vocabulary=self.terms_of_interest)
        self.transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
        self.tf = None
        self.idf = None
        self.max_idf = None
        self.weights = None

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
        self.weights = self.tf[:, indices] * (self.idf[indices] / self.max_idf)

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
