import ir_datasets
from aux_joblib import save_info_to_Joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import preprocess
from joblib import load
import load_tools


class corpus:
    def init(self, data_name, docs_num):
        loaded_data = ''
        if data_name == "":
            loaded_data = load(f'data_cranfield.joblib')
            
        else:
            load_tools._load(data_name,docs_num)
            loaded_data = load(f'data_{data_name}.joblib')

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