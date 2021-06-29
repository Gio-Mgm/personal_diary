
from app_modules import admin_add_user, user_dashboard, user_add_post
import streamlit as st
from scripts.functions import enc_values, dec_values
from scripts.CONST import PAGES, USER_OPTIONS, ADMIN_OPTIONS


st.set_page_config(
    page_title="Sentiment analysis",
    layout='wide',
    initial_sidebar_state='expanded'
)

# ----------------- #
#      SIDEBAR      #
# ----------------- #

page_select = st.sidebar.selectbox("Pages : ", PAGES)

# -------------- #
#      BODY      #
# -------------- #

#========================== PAGE UTILISATEUR =======================#


if page_select == PAGES[0]:
    user_id = st.text_input("user_id")
    if user_id:
        st.title("Utilisateur")
        option = st.radio("Menu", USER_OPTIONS)

        if option == USER_OPTIONS[0]:
            user_dashboard(user_id)

        if option == USER_OPTIONS[1]:
            user_add_post(user_id)


#======================= PAGE ADMINISTRATEUR =======================#

if page_select == PAGES[1]:
    st.title("Administration")

    col1, col2, col3 = st.beta_columns(3)
    
#with col1:

    option = st.radio("select", ADMIN_OPTIONS)
    
#with col2:
    st.subheader(option)
    if option == ADMIN_OPTIONS[0]:
        st.dataframe(dec_values("/users"))

    if option == ADMIN_OPTIONS[1]:
        admin_add_user()

    if option == ADMIN_OPTIONS[2]:
        with st.form("my_form"):
            name = st.text_input("Nom")
            submitted = st.form_submit_button("Submit")
        if submitted:
            data = {
                'email': email
            }
            
            enc_values("/users", data)
                
