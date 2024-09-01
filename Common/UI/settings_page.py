import streamlit as st 
import sysvariables as sv
import work_ai as ai


st.title("Системные настройки")


 
AIModels = st.session_state.settings["AImodel"]

 

try:
    indexAIModels = list(AIModels.keys()).index(st.session_state.current_model)
except:
    indexAIModels=0

col01, col02 = st.columns(2)
with col01:
    optionAImodels = st.selectbox("Рабочая AI-модель", (AIModels) , indexAIModels )
with col02:
    st.write(f"Выбрана: {optionAImodels} (путь: {AIModels[optionAImodels]})")
    if st.button("Перезагрузить модель", type="primary"):
        st.session_state.model = ai.reLoadModel(st.session_state.model, AIModels[optionAImodels])
        if (st.session_state.model==""):
            st.write(f"В памяти пока нет загруженных моделей")
        else:    
            st.write(f"Модель перезагружена")



st.session_state.current_model = optionAImodels
st.session_state.current_model_path = AIModels[optionAImodels]
st.session_state.settings["CurrentParameters"]["AImodel"] = optionAImodels


st.divider()


RAGBases = st.session_state.settings["RAGBases"]
 
 
col1, col2 = st.columns(2)
with col1:
 
    try:
       indexRAGBases = list(RAGBases.keys()).index(st.session_state.current_RAG_base)
    except:
        indexRAGBases=0
    optionRAGBases = st.selectbox( "Рабочая RAG база:", (RAGBases),indexRAGBases )
      
    st.session_state.current_RAG_base = optionRAGBases
    st.session_state.current_RAG_base_path = RAGBases[optionRAGBases]
    st.session_state.settings["CurrentParameters"]["RAGBase"] = optionRAGBases
    sv.saveSettings()



with col2:
    st.write(f"Информация о RAG базе '{optionRAGBases}':")
    st.write(f"Путь к размещению исходных документов: {RAGBases[optionRAGBases]["DOCPath"]}")
    st.write(f"Модель эмбедерра: {RAGBases[optionRAGBases]["Sentencer"]}")
    st.write(f"Путь к размещению базы: {RAGBases[optionRAGBases]["DBPath"]}")
    st.write(f"Название коллекции в базе: {RAGBases[optionRAGBases]["CollectionName"]}")
    st.write(f"Функция разбиения на чанки: {RAGBases[optionRAGBases]["Chuncker"]}")

st.divider()
sv.saveSettings()