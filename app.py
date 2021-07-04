"""app.py: Streamlit App"""

import streamlit as st
import time
import requests
import pandas as pd
from app_components import admin_add_user, admin_delete_user, admin_edit_user, admin_sentiment_analysis, admin_user_mood_date
from app_components import user_add_post, user_dashboard, user_edit_post, get_post_from_date
from scripts.CONST import ADMIN_SUB_OPTIONS, NOT_DIGIT, PAGES, PROCESSING, USER_NOT_EXISTS, USER_OPTIONS, ADMIN_OPTIONS, API_PATH


st.set_page_config(
    page_title="Personal_diary",
    page_icon=':neutral_face:',
    layout='centered',
    initial_sidebar_state='expanded'
)

if 'header' not in st.session_state:
	st.session_state.header = ADMIN_OPTIONS[0]

    

page_select = st.sidebar.radio("Pages : ", PAGES)

#========================== PAGE UTILISATEUR =======================#

if page_select == PAGES[0]:
    user_id = st.sidebar.text_input("user_id")
    if user_id:
        r = requests.get(API_PATH + f"/users/{user_id}")
        if not user_id.isdigit():
            st.error(NOT_DIGIT)
        elif r.status_code == 404:
            st.error(USER_NOT_EXISTS)
        else:
            res = r.json()
            option = st.sidebar.radio("Menu", USER_OPTIONS)

            if option == USER_OPTIONS[0]:
                user_dashboard(user_id, res)

            if option == USER_OPTIONS[1]:
                user_add_post(user_id)

            if option == USER_OPTIONS[2]:
                user_edit_post(user_id)

            if option == USER_OPTIONS[3]:
                get_post_from_date(user_id)


#======================= PAGE ADMINISTRATEUR =======================#

if page_select == PAGES[1]:
    title = st.header(st.session_state.header)
    option = st.sidebar.selectbox("Menu :", ADMIN_OPTIONS, key="header")

    with st.spinner(PROCESSING):
        r = requests.get(API_PATH + "/users/")
        res = r.json()
        res = pd.DataFrame(res)
        res = res[["user_id", "first_name",
                   "last_name", "email", "register_date"]]
        df = st.dataframe(res)
    
    if option == ADMIN_OPTIONS[0]:

        sub_option = st.selectbox("Choix de l'action à effectuer", ADMIN_SUB_OPTIONS, index=len(ADMIN_SUB_OPTIONS)-1)

        if sub_option == ADMIN_SUB_OPTIONS[0]:
            admin_add_user()

        if sub_option == ADMIN_SUB_OPTIONS[1]:
            admin_edit_user()

        if sub_option == ADMIN_SUB_OPTIONS[2]:
            admin_delete_user()

    if option == ADMIN_OPTIONS[1]:
        admin_sentiment_analysis()
    # st.subheader(option)
    # if option == ADMIN_OPTIONS[0]:
    #     admin_list_users()

    # if option == ADMIN_OPTIONS[1]:
    #     

    # if option == ADMIN_OPTIONS[2]:
    #     admin_edit_user()

    # if option == ADMIN_OPTIONS[3]:
    #     admin_delete_user()

    # if option == ADMIN_OPTIONS[4]:
    #     admin_user_mood_date()

    # if option == ADMIN_OPTIONS[5]:
    #     admin_mean_user()

    # if option == ADMIN_OPTIONS[6]:
    #     admin_mean_users()
