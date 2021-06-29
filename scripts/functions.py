import pandas as pd
import json, requests
import streamlit as st
import joblib

from scripts.CONST import API_PATH
from urllib.request import urlopen, Request
from urllib.parse import urlencode

def enc_values(endpoint: str, values: dict):
    url = API_PATH + endpoint
    data = urlencode(values).encode("latin-1")
    req = Request(url, data=data)
    return req  


def dec_values(endpoint: str):
    res = urlopen(API_PATH + endpoint)
    string = res.read().decode("latin-1")
    return json.loads(string)


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

def predict(text):
    model = joblib.load("models/LogisticRegression.joblib")
    x = bertify(text)
    pred = model.predict(x)
    prob = model.predict_proba(x)
    prob = pd.Series(data = prob[0], index=model.classes_)
    prob = prob.sort_values(ascending=False)
    print(prob)
    return pred, prob
