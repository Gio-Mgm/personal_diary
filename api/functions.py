from string import punctuation
import re  # regular expression
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk
from nltk.tokenize import word_tokenize
import pandas as pd
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
import joblib
def bertify(x):
    bert = joblib.load("models/bert.joblib")
    #bert = SentenceTransformer('paraphrase-MiniLM-L6-v2', device="cpu")
    if type(x) == str:
        X = bert.encode(x)
        X = X.reshape(1, -1)
    else:
        X = bert.encode(x.astype('str'))
    print("Encoded !")
    return X

def fit_score_model(model, X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=.2, random_state=1
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    return model

