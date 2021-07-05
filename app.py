"""app.py: Streamlit App"""

import streamlit as st
import requests
import pandas as pd
from app_components import UserComponents as uc, AdminComponents as ac
from scripts.CONST import ADMIN_SUB_OPTIONS, NOT_DIGIT, PAGES, PROCESSING, USER_HEADER, USER_SUBHEADER, USER_NOT_EXISTS, USER_OPTIONS, ADMIN_OPTIONS, API_PATH

st.set_page_config(
    page_title="Personal_diary",
    page_icon=':neutral_face:',
    layout='centered',
    initial_sidebar_state='expanded'
)
state = st.session_state

if 'user' not in state:
	state.user = None
if 'user_id' not in state:
	state.user_id = ""

user_comps = [
    uc.dashboard,
    uc.add_edit_post,
    uc.get_post
]
user_views = dict(zip(USER_OPTIONS, user_comps))


admin_sub_comps = [
    ac.add_user,
    ac.edit_user,
    ac.delete_user
]

admin_sub_views = dict(zip(ADMIN_SUB_OPTIONS, admin_sub_comps))

page = st.sidebar.radio("Pages : ", PAGES)

def user_id_listener():
    state.menu = USER_OPTIONS[0]
#========================== PAGE UTILISATEUR =======================#

if page == PAGES[0]:
    st.header(USER_HEADER)
    if not state.user_id:
        st.subheader(USER_SUBHEADER)
    user_id = st.sidebar.text_input(
        "Identifiant", 
        key="user_id", 
        on_change=user_id_listener
    )
    if user_id:
        if state.user == None or state.user_id != state.user["user_id"]:
            r = requests.get(API_PATH + f"/users/{user_id}")
            if not user_id.isdigit():
                st.error(NOT_DIGIT)
            elif r.status_code == 404:
                st.error(USER_NOT_EXISTS)
            else:
                state.user = r.json()
            view = st.sidebar.radio("Menu", tuple(user_views.keys()), key="menu")
        
        user_views[view](state)


#======================= PAGE ADMINISTRATEUR =======================#

if page == PAGES[1]:
    st.session_state.user_id = None
    st.session_state.user = None
    
    view = st.sidebar.selectbox("Menu :", ADMIN_OPTIONS, key="header")
    title = st.header(st.session_state.header)

    with st.spinner(PROCESSING):
        r = requests.get(API_PATH + "/users/")
        res = r.json()
        res = pd.DataFrame(res)
        res = res[["user_id", "first_name",
                   "last_name", "email", "register_date"]]
        df = st.dataframe(res)
    
    if view == ADMIN_OPTIONS[0]:
        
        sub_view = st.selectbox("Choix de l'action à effectuer", 
            tuple(admin_sub_views.keys()))

        admin_sub_views[sub_view]()

    if view == ADMIN_OPTIONS[1]:
        ac.mean_sentiments()
        
#st.sidebar.write(state)