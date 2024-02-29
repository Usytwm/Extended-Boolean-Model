# Cargando las bibliotecas
import ir_datasets
import nltk
import spacy as sp
import gensim
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# Cargar el diccionario de Gensim
from gensim.corpora import Dictionary


import ir_datasets
import nltk
import spacy as sp
import gensim
from gensim.corpora import Dictionary
import json


def build_vocabulary(dictionary):
    vocabulary = list(dictionary.token2id.keys())
    return vocabulary


def vector_representation(tokenized_docs, dictionary, vector_repr, use_bow=True):
    corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]

    if use_bow:
        vector_repr = corpus
    else:
        tfidf = gensim.models.TfidfModel(corpus)
        vector_repr = [tfidf[doc] for doc in corpus]

    return vector_repr


def pos_tagger_nltk(tokenized_docs):
    pos_tags = [nltk.pos_tag(doc) for doc in tokenized_docs]
    return pos_tags


def show(document):
    text = " ".join(document)
    wordcloud = WordCloud(
        width=800, height=800, background_color="white", min_font_size=10
    ).generate(text)

    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


# Intenta cargar documentos preprocesados y el diccionario
try:
    with open("src/proyect-code/Data/preprocessed_docs.json", "r") as f:
        tokenized_docs = json.load(f)

    dictionary = Dictionary.load("src/proyect-code/Data/dictionary.gensim")
    print("Documentos y diccionario cargados exitosamente.")
except FileNotFoundError:
    print(
        "No se encontró el archivo preprocessed_docs.json, comenzando preprocesamiento."
    )

    tokenized_docs = []
    vector_repr = []
    dictionary = {}
    vocabulary = []

    # Carga del corpus
    dataset = ir_datasets.load("cranfield")
    documents = [doc.text for doc in dataset.docs_iter()]
    print(f"Total de documentos: {len(documents)}")

    nltk.download("punkt")
    nltk.download("wordnet")
    nltk.download("stopwords")
    nltk.download("averaged_perceptron_tagger")

    nlp = sp.load("en_core_web_sm")

    def tokenization_nltk(texts):
        global tokenized_docs
        tokenized_docs = [nltk.tokenize.word_tokenize(doc) for doc in texts]
        return tokenized_docs

    def remove_noise_nltk(tokenized_docs):
        tokenized_docs = [
            [word.lower() for word in doc if word.isalpha()] for doc in tokenized_docs
        ]
        return tokenized_docs

    def remove_stopwords(tokenized_docs):
        stop_words = set(nltk.corpus.stopwords.words("english"))
        tokenized_docs = [
            [word for word in doc if word not in stop_words] for doc in tokenized_docs
        ]
        return tokenized_docs

    def morphological_reduction_nltk(tokenized_docs, use_lemmatization=True):
        if use_lemmatization:
            lemmatizer = nltk.stem.WordNetLemmatizer()
            tokenized_docs = [
                [lemmatizer.lemmatize(word) for word in doc] for doc in tokenized_docs
            ]
        else:
            stemmer = nltk.stem.PorterStemmer()
            tokenized_docs = [
                [stemmer.stem(word) for word in doc] for doc in tokenized_docs
            ]

        return tokenized_docs

    def filter_tokens_by_occurrence(tokenized_docs, no_below=5, no_above=0.5):
        global dictionary
        dictionary = gensim.corpora.Dictionary(tokenized_docs)
        dictionary.filter_extremes(no_below=no_below, no_above=no_above)

        filtered_words = [word for _, word in dictionary.iteritems()]
        filtered_tokens = [
            [word for word in doc if word in filtered_words] for doc in tokenized_docs
        ]

        return filtered_tokens

    # Ahora llamamos a cada función en el orden correcto
    tokenized_docs = tokenization_nltk(documents)
    tokenized_docs = remove_noise_nltk(tokenized_docs)
    tokenized_docs = remove_stopwords(tokenized_docs)
    tokenized_docs = morphological_reduction_nltk(tokenized_docs)
    tokenized_docs = filter_tokens_by_occurrence(tokenized_docs)
    vocabulary = build_vocabulary(dictionary)
    vector_repr = vector_representation(tokenized_docs, dictionary, vector_repr)
    pos_tags = pos_tagger_nltk(tokenized_docs)

    # Guarda los documentos preprocesados y el diccionario
    with open("src/proyect-code/Data/preprocessed_docs.json", "w") as f:
        json.dump(tokenized_docs, f)

    dictionary.save("src/proyect-code/Data/dictionary.gensim")
    print("Documentos preprocesados y diccionario guardados.")

# print(tokenized_docs[0])
print(dictionary)
