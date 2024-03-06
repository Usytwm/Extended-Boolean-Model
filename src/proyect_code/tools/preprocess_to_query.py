import nltk
import spacy

nlp = spacy.load("en_core_web_sm")


# Function to preprocess a single query
def preprocess_query(query):
    """Preprocesses a single query using tokenization, noise removal,
       stop word removal, and morphological reduction.

    Args:
        query (str): The query string to preprocess.

    Returns:
        list: A list of preprocessed tokens.
    """

    # Tokenize the query using spaCy
    tokenized_query = [token for token in nlp(query)]

    # Remove noise (keep only letters)
    tokenized_query = [token for token in tokenized_query if token.is_alpha]

    # Remove stop words (except for "and")
    stopwords = spacy.lang.en.stop_words.STOP_WORDS
    tokenized_query = [
        token for token in tokenized_query if token.text not in stopwords
    ]

    # Perform morphological reduction (lemmatization)
    tokenized_query = [token.lemma_ for token in tokenized_query]
    print(len(tokenized_query))
    return " ".join(tokenized_query)
