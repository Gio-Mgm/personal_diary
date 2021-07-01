import pandas as pd
import json, requests
import streamlit as st
import joblib

from scripts.CONST import API_PATH
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from emoji import demojize
import re

def enc_values(endpoint: str, values: dict):
    url = API_PATH + endpoint
    data = urlencode(values).encode("latin-1")
    req = Request(url, data=data)
    return req  


def dec_values(endpoint: str):
    res = urlopen(API_PATH + endpoint)
    string = res.read().decode("latin-1")
    return json.loads(string)


def clean_str(t):
    from nltk.corpus import stopwords
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
    bert = joblib.load("models/bert.joblib")
    #bert = SentenceTransformer('paraphrase-MiniLM-L6-v2', device="cpu")
    if type(x) == str:
        X = bert.encode(clean_str(x))
        X = X.reshape(1, -1)
    else:
        X = bert.encode(x.astype('str'))
    print("Encoded !")
    return X

def predict(text):
    model = joblib.load("models/LogisticRegression.joblib")
    x = bertify(text)
    pred = model.predict(x)
    prob = model.predict_proba(x)
    prob = pd.Series(data = prob[0], index=model.classes_)
    prob = prob.sort_values(ascending=False)
    print(prob)
    return pred, prob
