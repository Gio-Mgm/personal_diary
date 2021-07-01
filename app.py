
from app_components import *
import streamlit as st
import requests
from scripts.CONST import PAGES, USER_OPTIONS, ADMIN_OPTIONS, API_PATH


st.set_page_config(
    page_title="Personal_diary",
    page_icon='random',
    layout='wide',
    initial_sidebar_state='expanded'
)

page_select = st.sidebar.selectbox("Pages : ", PAGES)

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
            st.title("Utilisateur")
            option = st.sidebar.radio("Menu", USER_OPTIONS)

            if option == USER_OPTIONS[0]:
                user_dashboard(user_id, res)

            if option == USER_OPTIONS[1]:
                user_add_post(user_id)

            if option == USER_OPTIONS[2]:
                user_edit_post(user_id)

            if option == USER_OPTIONS[3]:
                user_get_dates(user_id)   


#======================= PAGE ADMINISTRATEUR =======================#

if page_select == PAGES[1]:
    st.title("Administration")

    #col1, col2, col3 = st.beta_columns(3)
    
#with col1:

    option = st.sidebar.radio("select", ADMIN_OPTIONS)
    
#with col2:
    st.subheader(option)
    if option == ADMIN_OPTIONS[0]:
        admin_list_users()

    if option == ADMIN_OPTIONS[1]:
        admin_add_user()

    if option == ADMIN_OPTIONS[2]:
        admin_edit_user()    
        
    if option == ADMIN_OPTIONS[3]:
        admin_delete_user()
                
    if option == ADMIN_OPTIONS[4]:
        admin_mean_user()    
        
    if option == ADMIN_OPTIONS[5]:
        admin_mean_users()
