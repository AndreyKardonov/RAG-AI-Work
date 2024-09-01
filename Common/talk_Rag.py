# Импорт библиотек
import streamlit as st 
import torch
import work_ai as ai
import work_rag as rag
import os




def openWindow(fname):
    os.startfile(fname )#"C://AI//RAG-docs//Стратагемы//Зенгер,Харро_фон_Стратагемы_Том_2_19_36_Подарочные_издания_Коллекция.pdf")


# -----------------------------------------------------------------------------
# --                     Секция работы со StreamLit                          --
# -----------------------------------------------------------------------------

torch.cuda.empty_cache()
#sv.initRAGPrompt()

# -----------------------------------------------------------------------------
# --                              Секция путей                               --
# -----------------------------------------------------------------------------

# Определяем пути до ИИ моделей


Sentencers = st.session_state.settings["Sentencer"]
RAGBases = st.session_state.settings["RAGBases"]

model_full_path = st.session_state.current_model_path
SentenceModelPath = "C:/AI/AI-models/Embeddings/multilingual-e5-large" # локальный путь для модели эмбедера
#SentenceModelPath = RAGBases[st.session_state.current_RAG_base]["Sentencer"]
DB_path = RAGBases[st.session_state.current_RAG_base]["DBPath"]
collection_name  = RAGBases[st.session_state.current_RAG_base]["CollectionName"]

 
print(model_full_path)

st.session_state.chroma_client = rag.initChroma(DB_path)
st.session_state.collection = rag.initCollection(st.session_state.chroma_client, collection_name)
st.session_state.SentenceModel = rag.initSentenceModel(SentenceModelPath)

if (st.session_state.model==""):
    st.session_state.model = ai.initModel(model_full_path)
    
st.title("Работа с RAG базой")
container = st.container(border=True) 

#container.write("База знаний Менеджера PM")
if container.button("Очистить чат"):
    if "rag_messages"  in st.session_state:
        st.session_state.rag_messages = []

 
# Initialize chat history
if "rag_messages" not in st.session_state:
    st.session_state.rag_messages = []

    # Display chat messages from history on app rerun
for message in st.session_state.rag_messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if (message["role"] == "assistant"):
#            with st.expander("Источники информации:"):
 #               st.write(message["metadata"])

            with st.expander("Источники информации:"):
                for m in message["metadata"]:
#                    st.button(m[0] + ", Страница: "+ str(m[1]), key=m[2], on_click = openWindow, args = (m[0],))
                    st.write(m[0] + ", Страница: "+ str(m[1]))


    # React to user input
if prompt := st.chat_input("Введите Ваш запрос к модели:"):
    chat_prompt = f"**{prompt}**"
    # Display user message in chat message container
    st.chat_message("user").write(chat_prompt)
      

    # Add user message to chat history
    st.session_state.rag_messages.append({"role": "user", "content": chat_prompt})
    response, metadata = rag.getRAGAnswer(st.session_state.model, prompt, st.session_state.collection, st.session_state.SentenceModel, 
                                st.session_state.Temperature, st.session_state.ChunksPutToModel, st.session_state.Distance  ) # Это главная функция, все остальное - обвязка!


    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.write(response)
        with st.expander("Источники информации:"):
            for m in metadata:
#                m[2]=st.session_state.Rag_topic_count
#                st.button(m[0] + ", Страница: "+ str(m[1]), key=m[2], on_click = openWindow, args = (m[0],))
#                st.session_state.Rag_topic_count +=1
                st.write(m[0] + ", Страница: "+ str(m[1]))


    # Add assistant response to chat history
    st.session_state.rag_messages.append({"role": "assistant", "content": response, "metadata":metadata})



