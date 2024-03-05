from process import corpus
import time


start = time.time()
_corpus = corpus()
_corpus.init(data_name="", docs_num=5)
end = time.time()
print(_corpus.docs)
#print(end-start)