"""app_components.py: generate parts of the Streamlit app."""

import streamlit as st
import pandas as pd
import requests
from datetime import date, timedelta
from scripts.CONST import ADD_POST, API_PATH, EDIT_POST, EMAIL_ALREADY_EXISTS, NOT_DIGIT, NO_POST, NO_POST_AT_DATE, PROCESSING, SENTIMENTS
from scripts.CONST import POST_ALREADY_EXISTS, POST_ADDED, POST_EDITED
from scripts.CONST import USER_ADDED, USER_DELETED, USER_EDITED, USER_NOT_EXISTS
from scripts.functions import make_pie_chart, predict

class UserComponents():
    def __init__(self):
        pass

    @staticmethod
    def dashboard(state):
        """
            user's dashboard view
        """
        user = state.user
        user_id = state.user_id
        bc = st.beta_container()
        bc.markdown(f"# _Bonjour {user['first_name']} {user['last_name']} !_")
        bc.markdown("________")
        st.markdown(f"_Email_ : {user['email']}")
        st.markdown(f"_Date d'inscription_ : {user['register_date']}")
        st.subheader("Dernier message")
        r = requests.get(API_PATH + f"/users/{user_id}/last/")
        res = r.json()
        if res:
            st.markdown(f"> {res[0]}")
            st.markdown(f"_Édité le : {res[1]}_")
        else:
            st.warning(NO_POST)
        return bc

    @staticmethod
    def add_edit_post(state):
        user_id = int(state.user_id)
        r = requests.get(API_PATH + f"/users/{user_id}/date/")
        st.write(r.status_code)
        st.write(r.text)
        is_add = False
        if r.status_code == 404:
            is_add = True
        else:
            res = r.json()
            st.markdown(f"> {res[0]}")
        with st.form(is_add and ADD_POST or EDIT_POST):
            text = st.text_input(is_add and ADD_POST or EDIT_POST)
            submitted = st.form_submit_button("Submit")
            if submitted:
                pred, prob = predict(text)
                data = {
                    'major': pred[0],
                    'text': text,
                    **prob
                }
                with st.spinner(PROCESSING):
                    if is_add:
                        r = requests.post(
                            API_PATH + f"/users/{user_id}/posts", json=data
                        )
                        st.success(POST_ADDED)
                    else:
                        r = requests.put(
                            API_PATH + f"/posts/{res['post_id']}", json=data
                        )
                        st.success(POST_EDITED)

    @staticmethod
    def get_post(state):
        """
            user's get post from date
        """
        user_id = state.user_id
        bc = st.beta_container()
        r = requests.get(API_PATH + f"/posts/{user_id}/dates")
        res = r.json()
        if not res:
            return bc.warning(NO_POST)
        dates = [""]
        for el in res:
            dates.append(el[0])
        date = bc.selectbox("Choisissez une date", dates, key="date")
        if date and int(state.user_id) == state.user["user_id"]:
            params = {
                "date":date
            }
            r = requests.get(API_PATH + f"/posts/{user_id}/date", params=params)
            bc.markdown(f"> {r.json()[0]}")
        return bc


class AdminComponents():

    def __init__(self):
        pass

    @staticmethod
    def add_user():
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


    @staticmethod
    def edit_user():
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

    @staticmethod
    def delete_user():
        """
            admin's delete user view
        """

        bc = st.beta_container()
        with bc.form("Supprimer"):
            user_id = st.text_input("Choix de l'id à supprimer")
            submitted = st.form_submit_button("Submit")
            if submitted:
                r = requests.get(API_PATH + f"/users/{user_id}")
                if not user_id.isdigit():
                    st.error(NOT_DIGIT)
                elif r.status_code == 404:
                    st.error(USER_NOT_EXISTS)
                else:
                    r = requests.delete(API_PATH + f"/users/{user_id}")
                    bc.info(USER_DELETED)
        return bc


    @staticmethod
    def user_sentiment():
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

    @staticmethod
    def mean_sentiments():
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
