import streamlit as st 
import json

#@st.cache_resource
def initVariables():
    if "settings_file" not in st.session_state:
        st.session_state.settings_file = "c:/ai/settings.json"
    if "current_model" not in st.session_state:
        st.session_state.current_model = ""
    if "current_model_path" not in st.session_state:
        st.session_state.current_model_path = ""
    if "current_RAG_base" not in st.session_state:
        st.session_state.current_RAG_base = ""
    if "current_RAG_base_path" not in st.session_state:
        st.session_state.current_RAG_base_path = ""
    if "Rag_topic_count" not in st.session_state:
        st.session_state.Rag_topic_count = 0

    if "settings" not in st.session_state:
        st.session_state.settings = ""
    if "baseName" not in st.session_state:
        st.session_state.baseName = ""
    if "docpath" not in st.session_state:
        st.session_state.docpath = ""
    if "ragpath" not in st.session_state:
        st.session_state.ragpath = ""
    if "chuncker" not in st.session_state:
        st.session_state.chuncker = ""


    if "chroma_db" not in st.session_state:
        st.session_state.chroma_db = ""
    if "sentencer" not in st.session_state:
        st.session_state.sentencer = ""
    if "sentencer_path" not in st.session_state:
        st.session_state.sentencer_path = ""
    if "collection_name" not in st.session_state:
        st.session_state.collection_name = ""

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = -1

    with open(st.session_state.settings_file, 'r') as fp:
        mySettings = json.load(fp)
    st.session_state.settings = mySettings

    CurrentParameters = st.session_state.settings["CurrentParameters"]
    st.session_state.current_model = CurrentParameters["AImodel"]
    AIModels = st.session_state.settings["AImodel"]
    st.session_state.current_model_path = AIModels[st.session_state.current_model ]
    st.session_state.current_RAG_base = CurrentParameters["RAGBase"]
    
    if "chroma_client" not in st.session_state:
        st.session_state.chroma_client = ""
    if "collection" not in st.session_state:
        st.session_state.collection = ""
    if "SentenceModel" not in st.session_state:
        st.session_state.SentenceModel = ""
    if "model" not in st.session_state:
        st.session_state.model = ""

    st.session_state.sysRAGPrompt = """
        Ты специалист консультант. Ответь на вопрос, базируясь только на этом контексте:

        {context}

        ---

        Ответь на вопрос, как можно подробнее, но не повторяясь, используя только контекст: {question}. Ответ должен быть развернутым и полным.
      """
    st.session_state.sysFreePrompt = """
        Ты специалист консультант. 

        Ответь на вопрос, как можно подробнее, но не повторяясь: {question}. Ответ должен быть развернутым и полным.
      """
    if "sysPrompt" not in st.session_state:
        st.session_state.sysPrompt = st.session_state.sysRAGPrompt
   # st.write(st.session_state.settings)

    if "Temperature" not in st.session_state:
        st.session_state.Temperature = st.session_state.settings["WorkParameters"]["Temperature"]
    if "ChunksPutToModel" not in st.session_state:
        st.session_state.ChunksPutToModel = st.session_state.settings["WorkParameters"]["ChunksPutToModel"]
    if "Distance" not in st.session_state:
        st.session_state.Distance = st.session_state.settings["WorkParameters"]["Distance"]




def saveSettings():
    with open(st.session_state.settings_file, 'w') as f:
        json.dump(st.session_state.settings, f)

