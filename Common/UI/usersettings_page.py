import streamlit as st 
import sysvariables as sv


st.title("Исследовательские настройки")

sysPrompt = st.text_area("Cистемное сообщение", value=st.session_state.sysPrompt, height=300)



col01, col02 = st.columns(2)
with col01:
    if st.button("Сохранить системное сообщение", type="primary"):
        st.session_state.sysPrompt = sysPrompt
        st.rerun()
        sv.saveSettings()
with col02:
    if st.button("Вернуть типовое системное сообщение", type="primary"):
        st.session_state.sysPrompt = st.session_state.sysRAGPrompt
        st.rerun()
        sv.saveSettings()

st.divider()


st.session_state.ChunksPutToModel = st.slider("Сколько чанков используется для поиска?", 3, 20, st.session_state.ChunksPutToModel)
st.session_state.Temperature = st.slider('Величина "Температуры"', 0.0, 1.0, st.session_state.Temperature)
st.session_state.Distance = st.slider('Величина "Дистанция" для поиска', 0.1, 0.8, st.session_state.Distance)


