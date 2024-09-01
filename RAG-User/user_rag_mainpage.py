# Импорт библиотек
import streamlit as st 
import torch
import sys # caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, 'C:/AI/Work/Common')
sys.path.insert(2, 'C:/AI/Work/Common/AI')
sys.path.insert(3, 'C:/AI/Work/Common/UI')
import sysvariables as sv



st.set_page_config(page_title="ИИ песочница", page_icon="🧊", layout="wide", initial_sidebar_state="expanded" )


sv.initVariables()
torch.cuda.empty_cache()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = -1
        st.rerun()


login_page        = st.Page("C:/AI/Work/Common/UI/login_page.py", title="SandBox", icon=":material/add_circle:")
logout_page       = st.Page(logout, title="Log out", icon=":material/logout:")
zettelcasten_page = st.Page("C:/AI/Work/Common/talk_Rag.py", title="Работа с RAG базой", icon=":material/add_circle:")
free_talk_page    = st.Page("C:/AI/Work/Common/talk_Free.py", title="Свободное общение", icon=":material/add_circle:")
settings_page     = st.Page("C:/AI/Work/Common/UI/settings_page.py", title="Системные настройки", icon=":material/add_circle:")
usersettings_page = st.Page("C:/AI/Work/Common/UI/usersettings_page.py", title="Исследовательские настройки", icon=":material/add_circle:")


st.sidebar.write(f"AI модель: {st.session_state.current_model}") 
st.sidebar.write(f"База знаний: {st.session_state.current_RAG_base }")
st.sidebar.write("---")
st.sidebar.write("Системный промпт:")
st.sidebar.write(st.session_state.sysPrompt)
st.sidebar.write("---")

if st.session_state.logged_in==0:
    pg = st.navigation(
        {
            "Настройка":         [settings_page, usersettings_page],
            "Работа с RAG":      [zettelcasten_page],
            "Работа с моделью":  [free_talk_page],
            "Аккаунт":           [logout_page],
        }
    )
else:
    if st.session_state.logged_in==1:
        pg = st.navigation(
            {
            "Настройка":         [usersettings_page],
            "Работа с RAG":      [zettelcasten_page],
            "Работа с моделью":  [free_talk_page],
            "Аккаунт":           [logout_page],
            }
        )
    else:
        pg = st.navigation([login_page])

pg.run()