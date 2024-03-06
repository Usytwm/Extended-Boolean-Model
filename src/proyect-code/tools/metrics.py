from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score


def precision(recovered_documents, relevant_documents):
    """
    Calcula la precisión de un conjunto de documentos recuperados frente a un conjunto de documentos relevantes.

    Args:
        recovered_documents (list): Identificadores de los documentos recuperados por el SRI.
        relevant_documents (list): Identificadores de los documentos relevantes.

    Returns:
        float: La precisión de los documentos recuperados, valor entre 0 y 1.
    """
    # Convertir listas de identificadores en etiquetas binarias
    # 1 para relevante, 0 para no relevante
    true_labels = [1 if doc in relevant_documents else 0 for doc in recovered_documents]

    # Calculamos precisión como en tu ejemplo original, pero con las etiquetas correctas
    # Nota: precision_score espera argumentos (y_true, y_pred)
    return precision_score(true_labels, [1] * len(recovered_documents))


def recall(recovered_documents, relevant_documents):
    """
    Calcula el recobrado (recall) de un conjunto de documentos recuperados frente a un conjunto de documentos relevantes.

    Args:
        recovered_documents (list): Identificadores de los documentos recuperados por el SRI.
        relevant_documents (list): Identificadores de los documentos relevantes.

    Returns:
        float: El recall de los documentos recuperados, valor entre 0 y 1.
    """
    # Calculamos recall manualmente ya que necesitamos considerar todos los documentos relevantes
    true_positives = len(set(recovered_documents) & set(relevant_documents))
    return true_positives / len(relevant_documents) if relevant_documents else 0


def f1(recovered_documents, relevant_documents):
    """
    Calcula la medida F1, que es el promedio armónico de la precisión y el recall, para un conjunto de documentos recuperados frente a un conjunto de documentos relevantes.

    Args:
        recovered_documents (list): Identificadores de los documentos recuperados por el SRI.
        relevant_documents (list): Identificadores de los documentos relevantes.

    Returns:
        float: La medida F1 de los documentos recuperados, valor entre 0 y 1.
    """
    prec = precision(recovered_documents, relevant_documents)
    rec = recall(recovered_documents, relevant_documents)
    if prec + rec == 0:
        return 0
    return 2 * (prec * rec) / (prec + rec)


def r_precision(recovered_documents, relevant_documents):
    """
    Calcula la R-Precisión, que es la precisión calculada en los primeros R documentos recuperados, donde R es el número total de documentos relevantes.

    Args:
        recovered_documents (list): Identificadores de los documentos recuperados por el SRI.
        relevant_documents (list): Identificadores de los documentos relevantes.

    Returns:
        float: La R-Precisión de los documentos recuperados, valor entre 0 y 1.
    """
    r = len(relevant_documents)
    # Recortar la lista de documentos recuperados a los primeros R elementos
    recovered_documents_at_r = recovered_documents[:r]
    return precision(recovered_documents_at_r, relevant_documents)


def fallout(recovered_documents, relevant_documents, total_documents):
    """
    Calcula el fallout, que es el número de documentos no relevantes recuperados dividido por el número total de documentos no relevantes.

    Args:
        recovered_documents (list): Identificadores de los documentos recuperados por el SRI.
        relevant_documents (list): Identificadores de los documentos relevantes.
        total_documents (int): El número total de documentos en el conjunto de datos.

    Returns:
        float: El fallout de los documentos recuperados, valor entre 0 y 1.
    """
    # total_documents es el número total de documentos en el conjunto de datos
    non_relevant_documents = total_documents - len(relevant_documents)
    false_positives = len(set(recovered_documents) - set(relevant_documents))
    if non_relevant_documents == 0:
        return 0
    return false_positives / non_relevant_documents


def calculate_metrics(recovered_documents, relevant_documents):
    """
    Calcula varias métricas de evaluación, incluyendo precisión, recall, F1, R-precisión, y fallout para un conjunto de documentos recuperados frente a un conjunto de documentos relevantes.

    Args:
        recovered_documents (list): Identificadores de los documentos recuperados por el SRI.
        relevant_documents (list): Identificadores de los documentos relevantes.

    Returns:
        dict: Un diccionario con las métricas calculadas (precision, recall, f1, r_precision, fallout).
    """
    # Convert lists to sets for efficient operations
    recovered_set = set(recovered_documents)
    relevant_set = set(relevant_documents)

    # True positives: Recovered documents that are relevant
    true_positives = len(recovered_set.intersection(relevant_set))
    print(" True positives : ",true_positives)
    # False positives: Recovered documents that are not relevant
    false_positives = len(recovered_set - relevant_set)
    print("false positives: ", false_positives)
    # False negatives: Relevant documents that were not recovered
    false_negatives = len(relevant_set - recovered_set)
    print("false negatives: ", false_negatives)
    # Precision
    precision = (
        true_positives / (true_positives + false_positives)
        if (true_positives + false_positives) > 0
        else 0
    )

    # Recall
    recall = (
        true_positives / (true_positives + false_negatives)
        if (true_positives + false_negatives) > 0
        else 0
    )

    # F1 Score
    f1 = (
        2 * (precision * recall) / (precision + recall)
        if (precision + recall) > 0
        else 0
    )

    # R-Precision (Precision at R, where R is the number of relevant documents)
    r_precision = precision  # In this simplified approach, R-Precision equals precision

    # Fallout
    total_non_relevant = (
        len(recovered_documents)
        + len(relevant_documents)
        - true_positives
        - false_negatives
    )
    fallout = (
        false_positives / (false_positives + total_non_relevant)
        if (false_positives + total_non_relevant) > 0
        else 0
    )

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "r_precision": r_precision,
        "fallout": fallout,
    }
