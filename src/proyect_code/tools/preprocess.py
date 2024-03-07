import nltk
import spacy as sp
import gensim
from wordcloud import WordCloud
import matplotlib.pyplot as plt




class Preprocess:
    def __init__(self):
        # Inicializar cualquier recurso global aquí, como el modelo spacy
        self.ensure_nltk_packages(
            ["punkt", "wordnet", "stopwords", "averaged_perceptron_tagger"]
        )
        # Inicializar el modelo de spaCy
        try:
            self.nlp = sp.load("en_core_web_sm")
        except Exception as e:
            sp.cli.download("en_core_web_sm")

        self.stop_words = set(nltk.corpus.stopwords.words("english"))

    def ensure_nltk_packages(self, packages):
        for package in packages:
            try:
                nltk.data.find(f"tokenizers/{package}")
            except LookupError:
                print(f"Descargando el paquete de NLTK: '{package}'")
                nltk.download(package)

    def tokenization_nltk(self, texts):
        return [nltk.tokenize.word_tokenize(doc) for doc in texts]

    def remove_noise_nltk(self, tokenized_docs):
        return [
            [word.lower() for word in doc if word.isalpha()] for doc in tokenized_docs
        ]

    def remove_stopwords(self, tokenized_docs):
        return [
            [word for word in doc if word not in self.stop_words]
            for doc in tokenized_docs
        ]

    def morphological_reduction_nltk(self, tokenized_docs, use_lemmatization=True):
        if use_lemmatization:
            lemmatizer = nltk.stem.WordNetLemmatizer()
            return [
                [lemmatizer.lemmatize(word) for word in doc] for doc in tokenized_docs
            ]
        else:
            stemmer = nltk.stem.PorterStemmer()
            return [[stemmer.stem(word) for word in doc] for doc in tokenized_docs]

    def filter_tokens_by_occurrence(self, tokenized_docs, no_below=5, no_above=0.5):
        dictionary = gensim.corpora.Dictionary(tokenized_docs)
        dictionary.filter_extremes(no_below=no_below, no_above=no_above)
        filtered_words = [word for _, word in dictionary.iteritems()]
        return [
            [word for word in doc if word in filtered_words] for doc in tokenized_docs
        ], dictionary

    def build_vocabulary(self, dictionary):
        return list(dictionary.token2id.keys())

    def vector_representation(self, tokenized_docs, dictionary, use_bow=True):
        corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]
        if use_bow:
            return corpus
        else:
            tfidf = gensim.models.TfidfModel(corpus)
            return [tfidf[doc] for doc in corpus]

    def pos_tagger_nltk(self, tokenized_docs):
        return [nltk.pos_tag(doc) for doc in tokenized_docs]

    def show_wordcloud(self, document):
        text = " ".join(document)
        wordcloud = WordCloud(
            width=800, height=800, background_color="white", min_font_size=10
        ).generate(text)
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()

    def preprocess_documents(self, documents, query):
        if query == False:
            tokenized_docs = self.tokenization_nltk(documents)
            tokenized_docs = self.remove_noise_nltk(tokenized_docs)
        
            tokenized_docs = self.remove_stopwords(tokenized_docs)
            tokenized_docs = self.morphological_reduction_nltk(tokenized_docs)
            tokenized_docs, dictionary = self.filter_tokens_by_occurrence(tokenized_docs)
            vocabulary = self.build_vocabulary(dictionary)
            vector_repr = self.vector_representation(tokenized_docs, dictionary)
            pos_tags = self.pos_tagger_nltk(tokenized_docs)
            tokenized_docs = [" ".join(doc) for doc in tokenized_docs]
            return tokenized_docs, dictionary, vocabulary, vector_repr, pos_tags
        else:
            tokenized_docs = documents.split()
 #           print("Remove nosise", tokenized_docs)
            
            tokenized_docs = [word.lower() for word in tokenized_docs if word.isalpha()]
            
            tokenized_docs = [word for word in tokenized_docs if word not in self.stop_words]
            
            lemmatizer = nltk.stem.WordNetLemmatizer()
            
            tokenized_docs = [lemmatizer.lemmatize(word) for word in tokenized_docs]
            
            tokenized_docs = " ".join(tokenized_docs)
            

            return tokenized_docs
        
