import streamlit as st
import altair as alt
from scripts.functions import enc_values, dec_values, predict

def user_dashboard(user_id):
    bc = st.beta_container()
    bc.subheader("Informations personnelles")
    response = dec_values("/users/"+user_id)
    for item in response.items():
        bc.markdown(f"_{item[0]}_ : {item[1]}")

    bc.subheader("messages")
    response = dec_values("/posts/"+user_id)
    text = response.pop("text")
    bc.text(text)
    bc.dataframe(response.items())
    #for item in response.items():
        #st.markdown(f"_{item[0]}_ : {item[1]}")
    return bc

def user_add_post(user_id):
    bc = st.beta_container()
    with bc.form("Ajout message"):
        text = st.text_area("Ajout message")
        submitted = st.form_submit_button("Submit")
        if submitted:
            pred, prob = predict(text)
            st.text(f"sentiment majeur : {pred}")
            for i, v in prob.iteritems():
                st.markdown(f"**{i}** : {round(v, 2)}")
            # data = {
            #     'text': text
            # }
            # req = enc_values(f"/users/{user_id}/posts", data)
            # bc.write(req)
    return bc

def admin_add_user():
    bc = st.beta_container()
    with bc.form("Add user"):
        email = st.text_input("Entrez l'adresse email")
        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            data = {
                'email': email
            }
            enc_values("/users/", data)
    return bc
