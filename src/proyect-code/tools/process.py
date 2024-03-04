import ir_datasets
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import preprocess

class corpus:
    def __init__(self, data_name=None, docs_num=None):
        if data_name is None:
            data_name = 'cranfield'
        # Cargar un conjunto de datos específico
        self.dataset = ir_datasets.load(data_name)
        # Obtener los documentos
        self.docs_iter = self.dataset.docs_iter()
        # Obtener cada texto por cada documento
        self.docs = [doc.text for doc in self.docs_iter]
        # Procesar los documentos
        self.preprocessed_docs = preprocess.preprocess_documents(self.docs,False)
        # Convertir cada lista de tokens en una cadena única
        self.preprocessed_docs = [' '.join(doc) for doc in self.preprocessed_docs]
        
        # Obtener queries
        self.queries = self.dataset.queries_iter()
        
        # Obtener resultados de cada query
        self.qrels = self.dataset.qrels_iter()
        
        # Crear el vectorizador y calcular la matriz TF-IDF
        self.tfidf_vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.preprocessed_docs)
    
        # Obtener el vocabulario
        self.vocabulary = self.tfidf_vectorizer.vocabulary_
        print('vocabulary: ', self.vocabulary)
        
        # Guardar los documentos preprocesados en un archivo pickle
        self.save_docs_to_pickle(self.preprocessed_docs, docs_num, data_name)
        
    def save_docs_to_pickle(self, docs, docs_num, data_name):
        # Asegurarse de que se especifica un número de documentos
        if docs_num is None:
            docs_num = len(docs)
        
        # Seleccionar el número especificado de documentos
        docs_to_save = docs[:docs_num]
        
        # Guardar los documentos seleccionados en un archivo pickle
        with open(f'{data_name}_docs.pkl', 'wb') as f:
            pickle.dump(docs_to_save, f)

    def print_qrels(self):
        # Iterar sobre las relaciones de relevancia (QRELs) para una consulta específica
        for query_id, doc_id, relevance in self.qrels:
            print(f"Query ID: {query_id}, Doc ID: {doc_id}, Relevance: {relevance}")
            
    def term_tfxidf(self, doc_index, term):
        # Encontrar el índice del término específico
        term_index = self.vocabulary.get(term)
        
        # Acceder al valor TF-IDF del término en el documento específico
        return self.tfidf_matrix[doc_index, term_index]
