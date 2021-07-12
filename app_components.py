"""app_components.py: generate parts of the Streamlit app."""

import streamlit as st
import pandas as pd
import requests
from src.utils.CONST import *
from datetime import date, timedelta
from src.utils.functions import make_pie_chart, predict

class UserComponents():
    def __init__(self):
        pass

    @staticmethod
    def dashboard(state):
        """
            dashboard view
        """
        user = state.user
        user_id = state.user_id
        bc = st.beta_container()
        bc.markdown(f"# _Bonjour {user['first_name']} {user['last_name']} !_")
        bc.markdown("________")
        bc.markdown(f"_Email_ : {user['email']}")
        bc.markdown(f"_Date d'inscription_ : {user['register_date']}")
        bc.subheader("Dernier message")
        r = requests.get(API_PATH + f"/users/{user_id}/last/")
        res = r.json()
        if res:
            st.markdown(f"> {res[0]}")
            st.markdown(f"_Édité le : {res[1]}_")
        else:
            st.warning(NO_POST)

    @staticmethod
    def add_edit_post(state):
        """
            add edit post view
        
        """
        
        user_id = state.user_id
        r = requests.get(API_PATH + f"/posts/{user_id}/date/")
        is_add = False
        if r.status_code == 404:
            is_add = True
            st.warning(NO_POST)
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
            user's get post from date view
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
            r = requests.get(
                API_PATH + f"/posts/{user_id}/date", params=params
            )
            bc.markdown(f"> {r.json()[0]}")
        return bc


class AdminComponents():

    def __init__(self):
        pass

    @staticmethod
    def get_user_infos():
        """
            get user's information and posts
        
        """
        bc = st.beta_container()
        user_id = bc.text_input("ID de l'utilisateur")
        if user_id:
            r = requests.get(API_PATH + f"/users/{user_id}")
            if not user_id.isdigit():
                bc.error(NOT_DIGIT)
            elif r.status_code == 404:
                bc.error(USER_NOT_EXISTS)
            else:
                res = r.json()
                col1, col2 = bc.beta_columns([.6, 1.4])
                with col1:
                    st.subheader("Informations personnelles")
                    st.markdown(f"_Prénom_ : {res['first_name']}")
                    st.markdown(f"_Nom_ : {res['last_name']}")
                    st.markdown(f"_Email_ : {res['email']}")
                    st.markdown(f"_Inscrit le_ : {res['register_date']}")
                r = requests.get(API_PATH + f"/users/{user_id}/posts")
                results = r.json()
                if results:
                    with col2:
                        for res in results:
                            st.markdown(f"> {res['text']}")
                            st.markdown(f"_Édité le : {res['date_last_updated']}_")
                            st.markdown(f"_Sentiment majoritaire : {res['major']}_")
                            st.markdown("___")
                else:
                    bc.warning(NO_POST)

    @staticmethod
    def add_user():
        """
            add user view
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
                res = r.json()
                st.write(res)
                if res == EMAIL_ALREADY_EXISTS:
                    st.error(res)
                else:
                    st.info(USER_ADDED)


    @staticmethod
    def edit_user():
        """
            edit user view
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
                        r = requests.put(
                            API_PATH + f"/users/{user_id}", params=data
                        )
                        bc.info(USER_EDITED)


    @staticmethod
    def delete_user():
        """
            delete user view
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



    @staticmethod
    def mean_sentiments():
        """
            sentiment analysis view
        
        """
        user_id = None
        checked = st.checkbox("Restreindre la requête à un utilisateur unique")
        with st.form("sentiment_analysis"):
            if checked:
                user_id = st.text_input("ID de l'utilisateur")
            dates = st.date_input("Choix de la période", value=(
                date.today() - timedelta(days=7), date.today()
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
                res_dict = dict(zip(SENTIMENTS, res))
                max_key = max(res_dict, key=res_dict.get)
                st.markdown(f"_Sentiment majoritaire : {max_key}_")
                st.pyplot(make_pie_chart(res_dict))
