import streamlit as st 
import json
import wx
import createRAG as cRG

app = wx.App(False)

st.header("Создание RAG базы")

st.divider()
col1, col2 = st.columns(2)


def checkCreate():
    if st.session_state.baseName == "": return -1
    if st.session_state.docpath == "": return -1
    if st.session_state.ragpath == "": return -1
    if st.session_state.sentencer == "": return -1
    if st.session_state.chuncker == "": return -1
    if st.session_state.collection_name == "": return -1
    return 0


Sentencers = st.session_state.settings["Sentencer"]
RAGBases = st.session_state.settings["RAGBases"]
Chunckers = st.session_state.settings["Chunckers"]

 
with col1:
    st.session_state.baseName = st.text_input("Введите название новой RAG базы ", st.session_state.baseName)
    st.session_state.collection_name = st.text_input("Введите название коллекции в новой RAG базы ", st.session_state.collection_name)

    optionSentencers = st.selectbox( "Какую модель эмбеддера выбираем?", (Sentencers) )
    st.session_state.sentencer=optionSentencers
    st.session_state.sentencer_path=Sentencers[optionSentencers]
    
    optionChunckers = st.selectbox( "Какую функцию разбиения на чанки выбираем?", (Chunckers) )
    st.session_state.chuncker=optionChunckers

    if st.button("Выберите путь к размещению исходных документов:"):
        dialog = wx.DirDialog(None, "Select a folder:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            st.session_state.docpath = dialog.GetPath()  

    if st.button("Выберите путь к размещению векторной базы данных (RAG):"):
        dialog = wx.DirDialog(None, "Select a folder:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            st.session_state.ragpath = dialog.GetPath()  
 

 
with col2: 
    st.write(f"Информация для создания новой RAG базы:")
    st.markdown(f"Имя базы: :red[{st.session_state.baseName}]")
    st.write(f"Название коллекции в базе: :red[{st.session_state.collection_name}]")
    st.write(f"Название используемого эмбедера: :red[{st.session_state.sentencer}]")
    st.write(f"Путь к используемому эмбедеру: :red[{st.session_state.sentencer_path}]")
    st.write(f"Название используемой функции разбиения на чанки : :red[{st.session_state.chuncker}]")
    st.write(f"Путь к размещению исходных документов: :red[{st.session_state.docpath}]")
    st.write(f"Путь к размещению базы: :red[{st.session_state.ragpath}]")
    
    if st.button("Создать базу", type="primary"):
        if checkCreate()==-1:
            st.error('Не все поля заполнены!', icon="🚨")
        else:
            st.write("Ожидаем.....")
            ret = cRG.createRAG( st.session_state.baseName, st.session_state.docpath, st.session_state.ragpath, st.session_state.sentencer, st.session_state.sentencer_path, st.session_state.collection_name, st.session_state.chuncker)
            st.write("База создана")
            st.write(ret)


st.divider()
col3, col4 = st.columns(2)

with col3: 
    optionRAGBases = st.selectbox( "Информация о существующих RAG базах", (RAGBases) )
    st.write(f"Имя базы: '{optionRAGBases}'")
    st.write(f"Путь к размещению исходных документов: {RAGBases[optionRAGBases]["DOCPath"]}")
    st.write(f"Модель эмбедерра: {RAGBases[optionRAGBases]["Sentencer"]}")
    st.write(f"Путь к размещению базы: {RAGBases[optionRAGBases]["DBPath"]}")
    st.write(f"Название коллекции в базе: {RAGBases[optionRAGBases]["CollectionName"]}")
    st.write(f"Функция разбиения на чанки: {RAGBases[optionRAGBases]["Chuncker"]}")

with col4: 
    if st.button("Обновить базу", type="secondary"):
        st.write("Ожидаем.....")
        ret = cRG.createRAG( optionRAGBases, RAGBases[optionRAGBases]["DOCPath"], RAGBases[optionRAGBases]["DBPath"], RAGBases[optionRAGBases]["Sentencer"], st.session_state.sentencer_path,RAGBases[optionRAGBases]["CollectionName"], RAGBases[optionRAGBases]["Chuncker"])
        st.write("База обновлена")
        st.write(ret)
    st.divider()

    if st.button("Удалить базу", type="primary"):
        st.write(f"Пока не работает )")

st.divider()

#filename = 'numbers.json'
#with open(filename, 'w') as f:
#    json.dump(mySettings, f)