"""app_components.py: generate parts of the Streamlit app."""

from re import sub
import time
import streamlit as st
import pandas as pd
import requests
from datetime import date, timedelta
from scripts.CONST import API_PATH, EMAIL_ALREADY_EXISTS, NOT_DIGIT, NO_POST, NO_POST_AT_DATE, PROCESSING, SENTIMENTS
from scripts.CONST import POST_ALREADY_EXISTS, POST_ADDED, POST_EDITED
from scripts.CONST import USER_ADDED, USER_DELETED, USER_EDITED, USER_NOT_EXISTS
from scripts.functions import make_pie_chart, predict



def user_dashboard(user_id, res):
    """
        user's dashboard view
    """

    bc = st.beta_container()
    bc.markdown(f"# _Bonjour {res['first_name']} {res['last_name']} !_")
    bc.markdown("________")
    st.markdown(f"_Email_ : {res['email']}")
    st.markdown(f"_Date d'inscription_ : {res['register_date']}")
    st.subheader("Dernier message")
    r = requests.get(API_PATH + f"/users/{user_id}/last/")
    res = r.json()

    if res:
        st.markdown(f"> {res[0]}")
        st.markdown(f"_Édité le : {res[1]}_")
    else:
        st.warning(NO_POST)
    return bc


def user_add_post(user_id):
    """
        user's add post view
    """
    empty = st.empty()
    with empty:
        r = requests.get(API_PATH + f"/users/{user_id}/dates")
        dates = [res[0] for res in r.json()]
        if str(date.today()) in dates:
            st.warning(POST_ALREADY_EXISTS)
        else:
            with st.form("Ajout message"):
                text = st.text_area("Ajout message")
                submitted = st.form_submit_button("Submit")
                if submitted:
                    pred, prob = predict(text)
                    data = {
                        'major': pred[0],
                        'text': text,
                        **prob
                    }
                    # for i, v in prob.iteritems():
                    #     st.markdown(f"**{i}** : {round(v, 2)}")
                    with st.spinner(PROCESSING):
                        r = requests.post(API_PATH + f"/users/{user_id}/posts", json=data)
                    st.success(POST_ADDED)



def user_edit_post(user_id):
    """
        user's edit post view
    """

    r = requests.get(API_PATH + f"/users/{user_id}/{date.today()}")
    res = r.json()
    st.write(r.status_code)
    st.write(r.text)
    bc = st.beta_container()
    if r.status_code == 404:
        return bc.warning(NO_POST_AT_DATE)
    bc.markdown(f"> {res[0]}")
    with bc.form("Modifier message"):
        text = st.text_input("Modifier message")
        submitted = st.form_submit_button("Submit")
        if submitted:
            pred, prob = predict(text)
            data = {
                'major': pred[0],
                'text': text,
                **prob
            }
            r = requests.put(API_PATH + f"/posts/{res['post_id']}", json=data)
            st.info(POST_EDITED)
    return bc


def get_post_from_date(user_id):
    """
        user's get post from date
    """

    bc = st.beta_container()
    r = requests.get(API_PATH + f"/posts/{user_id}/dates")
    res = r.json()
    if not res:
        return bc.warning(NO_POST)
    dates = [""]
    for el in res:
        dates.append(el[0])
    date = bc.selectbox("Choisissez une date", dates)
    if date:
        params = {
            "date": date
        }
        r = requests.get(API_PATH + f"/posts/{user_id}/{date}")
        bc.markdown(f"> {r.json()[0]}")

    return bc


def admin_add_user():
    """
        admin's add user view
    """

    with st.form("Add user"):
        email = st.text_input("email")
        fn = st.text_input("prénom")
        ln = st.text_input("nom")
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            data = {
                'email': email,
                'first_name': fn,
                'last_name': ln
            }
            r = requests.post(API_PATH + "/users/", json=data)
            if r.status_code == 500:
                st.error(EMAIL_ALREADY_EXISTS)
            else:
                st.info(USER_ADDED)



def admin_edit_user():
    """
        admin's edit user view
    """

    bc = st.beta_container()
    user_id = bc.text_input("ID de l'utilisateur")
    if user_id:
        r = requests.get(API_PATH + f"/users/{user_id}")
        if not user_id.isdigit():
            st.error(NOT_DIGIT)
        elif r.status_code == 404:
            st.error(USER_NOT_EXISTS)
        else:
            res = r.json()
            with bc.form("Add user"):
                fn = st.text_input("Prénom", value=res["first_name"])
                ln = st.text_input("Nom", value=res["last_name"])
                email = st.text_input("email", value=res["email"])

                submitted = st.form_submit_button("Submit")
                if submitted:
                    data = {
                        'email': email,
                        'first_name': fn,
                        'last_name': ln
                    }
                    r = requests.put(API_PATH + "/users", json=data)
                    bc.info(USER_EDITED)
    return bc


def admin_delete_user():
    """
        admin's delete user view
    """

    bc = st.beta_container()
    with bc.form("Supprimer"):
        user_id = st.text_input("Choix de l'id à supprimer")
        submitted = st.form_submit_button("Submit")
        if submitted:
            r = requests.delete(API_PATH + f"/users/{user_id}")
            res = r.json()
            if user_id:
                if not user_id.isdigit():
                    st.error(NOT_DIGIT)
                elif not user_id in res["user_id"]:
                    st.error(USER_NOT_EXISTS)
                else:
                    bc.info(USER_DELETED)
    return bc

def admin_user_mood_date():
    """
        visualize text and emotions of an user
        at a precise date
    """
    import matplotlib.pyplot as plt
    bc = st.beta_container()
    col1, col2 = st.beta_columns(2)
    user_id = bc.text_input("ID de l'utilisateur")
    if user_id:
        r = requests.get(API_PATH + f"/users/{user_id}/posts")
        if not user_id.isdigit():
            return bc.error(NOT_DIGIT)
        elif r.status_code == 404:
            return bc.error(USER_NOT_EXISTS)
        elif not r.json():
            return bc.warning(NO_POST)
        res = r.json()
        dates = []
        for el in res:
            dates.append(el["date_last_updated"])
        with col1:
            date = bc.selectbox("Choisissez une date", dates)
            if date:
                params = {
                    "user_id": user_id,
                    "date": date,
                    "admin": True
                }               
                r = requests.get(API_PATH + "/posts/user_id/date/", params=params)
                res= r.json()
                sub_res = {key: round(val,3) for key, val in res.items() if key in SENTIMENTS}
            st.markdown(f"> {res['text']}")
            st.markdown(f"_Sentiment majoritaire : {res['major']}_")
        with col2:
            st.pyplot(make_pie_chart(sub_res))
    return bc



def admin_sentiment_analysis():
    """
        sentiment analysis view
    
    """
    #bc = st.beta_container()
    user_id = None
    checked = st.checkbox("Restreindre la requête à un utilisateur unique")
    with st.form("sentiment_analysis"):
        if checked:
            user_id = st.text_input("ID de l'utilisateur")
        dates = st.date_input("Choix de la période", value=(
            date.today() - timedelta(days=1), date.today()
        ), max_value=date.today())
        submitted = st.form_submit_button("Submit")
    if submitted:
        params = {
            "start": dates[0],
            "end": dates[1]
        }
        if user_id:
            r = requests.get(API_PATH + f"/users/{user_id}")
            if not user_id.isdigit():
                st.error(NOT_DIGIT)
            elif r.status_code == 404:
                st.error(USER_NOT_EXISTS)
            else:
                params['user_id'] = user_id

        r = requests.get(API_PATH + "/posts/sentiments/", params=params)
        
        if r.status_code == 200:
            res = r.json()[0]
            s = pd.Series(res, index=SENTIMENTS)
            st.dataframe(s)
            st.markdown(f"_Sentiment majoritaire : {s.idxmax()}_")
