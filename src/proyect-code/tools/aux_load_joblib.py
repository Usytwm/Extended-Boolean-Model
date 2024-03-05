import ir_datasets
from aux_save_joblib import save_info
from sklearn.feature_extraction.text import TfidfVectorizer
import preprocess
from joblib import dump

def load_info(data,docs_num):
    data_name = data
    # Cargar un conjunto de datos específico
    dataset = ir_datasets.load(data_name)
    # Obtener los documentos
    docs_iter =  dataset.docs_iter()
    # Obtener cada texto por cada documentos
    docs = [doc.text for doc in docs_iter]
    # Procesar los documentos
    preprocessed_docs = preprocess.preprocess_documents(docs,False)
    # Convertir cada lista de tokens en una cadena única
    preprocessed_docs = [' '.join(doc) for doc in preprocessed_docs]

     # Obtener queries
    queries = dataset.queries_iter()

    # Obtener resultados de cada query
    qrels = dataset.qrels_iter()

    data_to_save = {
        'preprocessed_docs': preprocessed_docs,
        'queries': list(queries),
        'qrels': list(qrels),
        'docs' : docs,
        'data_name' : data_name
        #'dataset' : dataset,
        #'docs_iter': docs_iter
    }

    dump(data_to_save, f'data_{data}.joblib')
    # Crea un jblin con los valores de tfxidf con la coleccion de documentos y se puede modificar la cantidad de documentos a escoger 
    save_info(docs, docs_num, data_name)
    # Guardar los datos en un archivo