import streamlit as st
st.title("Авторизация")
username = st.text_input("Код доступа")
#password = st.text_input("Password", type="password")
 
if st.button("Login"):
#    if username == "user" and password =="":
    if username == "AdminAI":
        st.success("Logged in successfully.")
        st.session_state.logged_in = 0
        st.rerun()
    else:
        if username == "UserAI":
            st.success("Logged in successfully.")
            st.session_state.logged_in = 1
            st.rerun()
        else:
            st.error("Invalid username.")

