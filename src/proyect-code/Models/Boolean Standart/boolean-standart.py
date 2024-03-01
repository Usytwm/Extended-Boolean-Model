class Boolean_model:

    def __init__(self, documents):
        self.documents=documents
        self.tokens_list = {}

    def load_documents(self, documents)-> dict:
        tokens_list = {}

        for doc in documents:
            tokens = set(doc.text)
            for token in tokens:
                if not tokens_list.__contains__(token):
                    tokens_list[token] = [doc]
                else:
                    tokens_list[token].append(doc)

        print(tokens_list)

        return tokens_list


    def load_query(self, query):
        result = []
        for i, token in enumerate(query):
            result.append(token)
            if i == len(query) - 1:
                continue
            if not(query[i] in ("and", "or", "not")) and not query[i+1] in ("and", "or", "not"):
                result.append("and")

        return result

    def similitud(self, query, token_list):
        print("Empieza el metodo")
        print(query)
        print(token_list)
        if query[0] == "not":
            result=set(self.documents).difference(set(token_list[query[1]]))
        else:
            result=set(token_list[query[0]])
        
        print(result)
        for i, token in enumerate(query): # Procesando or
            if token == "or":
                if query[i+1] == "not":
                    result=result.union((set(self.documents)).difference(set(token_list[query[i+2]])))
                else:
                    result=result.union(set(token_list[query[i+1]]))
            elif token == "and":
                if query[i+1] == "not":
                    result=result.intersection(set(self.documents).difference(set(token_list[query[i+2]])))
                else:
                    result=result.intersection(set(token_list[query[i+1]]))
            print(result)

        print("Resultado")
        print(result)
        return result





