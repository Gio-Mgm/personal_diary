"""functions.py: Utils function for predictions."""

import re
import joblib
import pandas as pd
import matplotlib.pyplot as plt
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

    # SentenceTransformer('paraphrase-MiniLM-L6-v2')
    bert = joblib.load("models/bert.joblib")
    if isinstance(x, str):
        X = bert.encode(clean_str(x))
        X = X.reshape(1, -1)
    else:
        X = bert.encode(x.astype('str'))
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
    return pred, prob


def make_pie_chart(data):
    """
        Plot a pie chart of sentiments
    
    """
    
    rates = data.values()
    plt.figure(figsize=(5, 5))
    plt.pie(rates, normalize=True, radius=1.1, labeldistance=1.05, labels=data.keys())
    plt.title('Répartition des émotions')
    my_circle = plt.Circle((0, 0), .5, color='white')
    p = plt.gcf()
    p.gca().add_artist(my_circle)
    labels = [f"{item[0]} : {round(item[1], 2)}%" for item in data.items()]
    plt.legend(labels, loc='best',
               bbox_to_anchor=(.7, 0., 1, 0.8))
    plt.axis('equal')
    fig = plt.gcf()
    plt.close()
    return fig
