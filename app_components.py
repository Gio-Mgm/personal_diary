"""app_components.py: generate parts of the Streamlit app."""

import streamlit as st
import pandas as pd
import requests
from scripts.CONST import API_PATH, EMAIL_ALREADY_EXISTS, NOT_DIGIT, NO_POST
from scripts.CONST import POST_ALREADY_EXISTS, POST_ADDED, POST_EDITED
from scripts.CONST import USER_ADDED, USER_DELETED, USER_EDITED, USER_NOT_EXISTS
from scripts.functions import predict


def user_dashboard(user_id, res):
    """
        user's dashboard view
    """

    bc = st.beta_container()
    col1, col2 =st.beta_columns(2)
    with col1:
        st.subheader("Informations personnelles")
        st.markdown(f"_Prénom_ : {res['first_name']}")
        st.markdown(f"_Nom_ : {res['last_name']}")
        st.markdown(f"_Email_ : {res['email']}")
        st.markdown(f"_Inscrit le_ : {res['register_date']}")
    with col2:
        st.subheader("Dernier message")
        r = requests.get(API_PATH + f"/users/{user_id}/post")
        if r.json():
            st.markdown(f"> {r.json()['text']}")
            st.markdown(f"_{r.json()['date_last_updated']}_")
        else:
            st.warning(NO_POST)
    return bc


def user_add_post(user_id):
    """
        user's add post view
    """

    bc = st.beta_container()
    r = requests.get(API_PATH + f"/users/{user_id}/post")
    res = r.json()
    if res:
        bc.warning(POST_ALREADY_EXISTS)
    else:
        with bc.form("Ajout message"):
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
                r = requests.post(API_PATH + f"/users/{user_id}/posts", json=data)
                st.info(POST_ADDED)
    return bc


def user_edit_post(user_id):
    """
        user's edit post view
    """

    bc = st.beta_container()
    r = requests.get(API_PATH + f"/users/{user_id}/post")
    res = r.json()
    if not res:
        return bc.warning(NO_POST)
    bc.markdown(f"> {res['text']}")
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


def user_get_dates(user_id):
    """
        user's get post by date view
    """

    bc = st.beta_container()
    r = requests.get(API_PATH + f"/users/{user_id}/by_dates")
    res = r.json()
    if not res:
        return bc.warning(NO_POST)
    dates = [""]
    for el in res:
        dates.append(el[0])
    date = bc.selectbox("Choisissez une date", dates)
    if date:
        r = requests.get(API_PATH + f"/users/{user_id}/by_dates/{date}")
        bc.markdown(f"> {r.json()[0]}")

    return bc


def admin_list_users():
    """
        admin's list users view
    """

    bc = st.beta_container()
    r = requests.get(API_PATH + "/users/")
    for item in r.json():
        bc.markdown("________")
        bc.markdown(f"_ID_ : {item['user_id']}")
        bc.markdown(f"_Prénom_ : {item['first_name']}")
        bc.markdown(f"_Nom_ : {item['last_name']}")
        bc.markdown(f"_Email_ : {item['email']}")
        bc.markdown(f"_Inscrit le_ : {item['register_date']}")
    return bc


def admin_add_user():
    """
        admin's add user view
    """

    bc = st.beta_container()
    with bc.form("Add user"):
        email = st.text_input("email")
        fn = st.text_input("prénom")
        ln = st.text_input("nom")
        # Every form must have a submit button.
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
        return bc


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
    r = requests.get(API_PATH + "/users/")
    res = r.json()
    res = pd.DataFrame(res)
    res = res[["user_id", "first_name", "last_name", "email"]]
    bc.dataframe(res)
    with bc.form("Supprimer"):
        user_id = st.text_input("Choix de l'id à supprimer")
        submitted = st.form_submit_button("Submit")
        if submitted:
            r = requests.delete(API_PATH + f"/users/{user_id}")
            if user_id:
                if not user_id.isdigit():
                    st.error(NOT_DIGIT)
                elif not user_id in res["user_id"]:
                    st.error(USER_NOT_EXISTS)
                else:
                    bc.info(USER_DELETED)
    return bc

def admin_mean_user():
    """
        admin's mean user view
    """


def admin_mean_users():
    """
        admin's means users view
    """
