# Импорт библиотек
import streamlit as st 
import torch
import work_ai as ai
import work_rag as rag

torch.cuda.empty_cache()

if (st.session_state.model==""):
    st.session_state.model = ai.initModel(st.session_state.current_model_path)
    
st.title("Свободное общение на любые темы")
container = st.container(border=True) 

if "messages" not in st.session_state: # Создаем пустую историю чата
    st.session_state.messages = []

if container.button("Очистить чат"): # Очищаем историю чата по нажатию кнопки
    st.session_state.messages = []

for message in st.session_state.messages: # Выводим историю чата на экран
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Введите Ваш запрос к модели:"): # Если пользователь что-тот ввел, то...
    chat_prompt = f"**{prompt}**"
    st.chat_message("user").write(chat_prompt) # Выводим сообщение пользователя на экран
    st.session_state.messages.append({"role": "user", "content": chat_prompt})# Добавляем вопросо пользователя в хистори чата
    response = rag.getFreeAnswer(st.session_state.model, prompt, st.session_state.sysFreePrompt, st.session_state.Temperature) # Это главная функция, все остальное - обвязка!
    with st.chat_message("assistant"): # Выводим ответ чат-бота
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response}) # Добавляем ответ чат-бота в хистори чата

        
    

