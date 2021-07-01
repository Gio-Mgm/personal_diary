"""functions.py: Utils function for predictions."""

import re
import joblib
import pandas as pd
from emoji import demojize

def clean_str(t):
    """
        clean and lemmatize text

    """

    # Lowercasing
    t = t.lower()

    # Remove special chars
    t = re.sub(r"(http|@)\S+", "",t)
    t = demojize(t)
    t = re.sub(r"::", ": :", t)
    t = re.sub(r"’", "'", t)
    t = re.sub(r"[^a-z\':_]", " ", t)

    # Remove repetitions
    pattern = re.compile(r"(.)\1{2,}", re.DOTALL)
    t = re.sub(pattern, r"\1", t)

    # Transform short negation form
    t = re.sub(r"(can't|cannot)", 'can not', t)
    t = re.sub(r"(ain't|wasn't|weren't)", 'be not', t)
    t = re.sub(r"(don't|didn't|didnt)", 'do not', t)
    t = re.sub(r"(haven't|hasn't)", 'have not', t)
    t = re.sub(r"(won't)", 'will not', t)
    t = re.sub(r"(im)", ' i am', t)
    t = re.sub(r"(ive)", ' i have', t)
    t = re.sub(r"(n't)", ' not', t)
    return t


def bertify(x):
    """
        Encode lemmatized text with bert

    """

    bert = joblib.load("models/bert.joblib")
    #bert = SentenceTransformer('paraphrase-MiniLM-L6-v2', device="cpu")
    if isinstance(x) == str:
        X = bert.encode(clean_str(x))
        X = X.reshape(1, -1)
    else:
        X = bert.encode(x.astype('str'))
    print("Encoded !")
    return X


def predict(text):
    """
        Make predictions and return it
        with probabilities
    """

    model = joblib.load("models/LogisticRegression.joblib")
    x = bertify(text)
    pred = model.predict(x)
    prob = model.predict_proba(x)
    prob = pd.Series(data = prob[0], index=model.classes_)
    prob = prob.sort_values(ascending=False)
    print(prob)
    return pred, prob
