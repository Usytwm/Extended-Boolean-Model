# Cargando las bibliotecas
import ir_datasets
import nltk
import spacy as sp
import gensim

nltk.download("punkt")
nltk.download("wordnet")
nltk.download("stopwords")
nltk.download("averaged_perceptron_tagger")

# Cargar el corpus y mostrar un documento
dataset = ir_datasets.load("cranfield")

documents = [doc.text for doc in dataset.docs_iter()]

print(len(documents))

tokenized_docs = []
vector_repr = []
dictionary = {}
vocabulary = []

nlp = sp.load("en_core_web_sm")


def tokenization_spacy(texts):
    return [[token for token in nlp(doc)] for doc in texts]


tokenization_spacy(documents)


def tokenization_nltk(texts):
    global tokenized_docs
    tokenized_docs = [nltk.tokenize.word_tokenize(doc) for doc in texts]
    return tokenized_docs


tokenization_nltk(documents)


def remove_noise_spacy(tokenized_docs):
    return [[token for token in doc if token.is_alpha] for doc in tokenized_docs]


remove_noise_spacy(tokenization_spacy(documents))


def remove_noise_nltk(tokenized_docs):
    tokenized_docs = [
        [word.lower() for word in doc if word.isalpha()] for doc in tokenized_docs
    ]
    return tokenized_docs


remove_noise_nltk(tokenized_docs)


def remove_stopwords_spacy(tokenized_docs):
    stopwords = sp.lang.en.stop_words.STOP_WORDS
    return [
        [token for token in doc if token.text not in stopwords]
        for doc in tokenized_docs
    ]


remove_stopwords_spacy(remove_noise_spacy(tokenization_spacy(documents)))


def remove_stopwords(tokenized_docs):
    stop_words = set(nltk.corpus.stopwords.words("english"))
    tokenized_docs = [
        [word for word in doc if word not in stop_words] for doc in tokenized_docs
    ]
    return tokenized_docs


remove_stopwords(tokenized_docs)


def morphological_reduction_spacy(tokenized_docs, use_lemmatization=True):
    stemmer = nltk.stem.PorterStemmer()
    return [
        [
            token.lemma_ if use_lemmatization else stemmer.stem(token.text)
            for token in doc
        ]
        for doc in tokenized_docs
    ]


morphological_reduction_spacy(
    remove_stopwords_spacy(remove_noise_spacy(tokenization_spacy(documents))), True
)


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


morphological_reduction_nltk(tokenized_docs)


def filter_tokens_by_occurrence(tokenized_docs, no_below=5, no_above=0.5):
    global dictionary
    dictionary = gensim.corpora.Dictionary(tokenized_docs)
    dictionary.filter_extremes(no_below=no_below, no_above=no_above)

    filtered_words = [word for _, word in dictionary.iteritems()]
    filtered_tokens = [
        [word for word in doc if word in filtered_words] for doc in tokenized_docs
    ]

    return filtered_tokens


tokenized_docs = filter_tokens_by_occurrence(tokenized_docs)


def build_vocabulary(dictionary):
    vocabulary = list(dictionary.token2id.keys())
    return vocabulary


vocabulary = build_vocabulary(dictionary)


def vector_representation(tokenized_docs, dictionary, vector_repr, use_bow=True):
    corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]

    if use_bow:
        vector_repr = corpus
    else:
        tfidf = gensim.models.TfidfModel(corpus)
        vector_repr = [tfidf[doc] for doc in corpus]

    return vector_repr


vector_repr = vector_representation(tokenized_docs, dictionary, vector_repr)


def pos_tagger_spacy(tokenized_docs):
    return [[(token.text, token.tag_) for token in doc] for doc in tokenized_docs]


pos_tags = pos_tagger_spacy(tokenization_spacy(documents))


def pos_tagger_nltk(tokenized_docs):
    pos_tags = [nltk.pos_tag(doc) for doc in tokenized_docs]
    return pos_tags


pos_tags = pos_tagger_nltk(tokenized_docs)

from wordcloud import WordCloud
import matplotlib.pyplot as plt


def show(document):
    text = " ".join(document)
    wordcloud = WordCloud(
        width=800, height=800, background_color="white", min_font_size=10
    ).generate(text)

    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


show(tokenized_docs[0])
