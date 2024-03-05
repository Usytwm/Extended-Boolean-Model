import ir_datasets
from aux_save_joblib import save_info
from aux_load_joblib import load_info
from sklearn.feature_extraction.text import TfidfVectorizer
import preprocess
from joblib import load


class corpus:
    def __init__(self, data_name, docs_num):
        loaded_data = ''
        if data_name == "":
            data_name = 'cranfield'
            loaded_data = load(f'data_{data_name}.joblib')
            data_name = loaded_data['data_name']
            
        else:
            load_info(data_name,docs_num)
            loaded_data = load(f'data_{data_name}.joblib')

        # Cargar los datos desde el archivo

        # Cargar un conjunto de datos específico
        #self.dataset = loaded_data['dataset']
        # Obtener los documentos
        #self.docs_iter = loaded_data['docs_iter']
        # Obtener cada texto por cada documentos
        self.docs = loaded_data['docs']
        self.preprocessed_docs = loaded_data['preprocessed_docs']
        
        # Obtener queries
        self.queries = loaded_data['queries']
        
        # Obtener resultados de cada query
        self.qrels = loaded_data['qrels']
        
    def print_qrels(self):
        # Iterar sobre las relaciones de relevancia (QRELs) para una consulta específica
        for query_id, doc_id, relevance in self.qrels:
            print(f"Query ID: {query_id}, Doc ID: {doc_id}, Relevance: {relevance}")
            