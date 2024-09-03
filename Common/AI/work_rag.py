import streamlit as st 
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import logging

# -----------------------------------------------------------------------------
# --                       Секция констант/переменных                        --
# -----------------------------------------------------------------------------

 
top_k=30
top_p=0.9
repeat_penalty=1.1

PROMPT_TEMPLATE = st.session_state.sysPrompt

# -----------------------------------------------------------------------------
# --                Секция инициализации хранилища и модели                  --
# -----------------------------------------------------------------------------
# префикс @st.cache_resource используется для кеширования функции Streamlit ом

@st.cache_resource
def initChroma(DB_path):     # Создание клиента Chroma для работы с постоянным хранилищем (PersistentClient)
    chroma_client = chromadb.PersistentClient(path=DB_path)#, settings=Settings(anonymized_telemetry=False))
    return chroma_client

@st.cache_resource
def initCollection(_chroma_client, collection_name):        # Получение коллекции из векторной базы данных
    collect = _chroma_client.get_or_create_collection(name=collection_name)
    return collect

@st.cache_resource
def initSentenceModel(SentenceModelPath):     # Инициализация модели для работфы с word embedding
    SentenceModel = SentenceTransformer(SentenceModelPath) 
    return SentenceModel


    
# -----------------------------------------------------------------------------
# --                     Секция вспомогательных процедур                     --
# -----------------------------------------------------------------------------

# Функция для поиска и генерации промпта на основе контекста
def search_and_generate_rag_prompt(question, collection, SentenceModel, distance_threshold, n_results):
    # Оцифровка текста запроса и преобразование его в список
    query_embedding = SentenceModel.encode([question])[0].tolist()


    # Запрос к коллекции для поиска документов, которые наиболее близки к запросу
    results = collection.query(
        query_embeddings=[query_embedding],  # Векторное представление текста запроса в виде списка
        n_results=n_results  # Количество возвращаемых результатов
    )
    print (results['distances'][0]) # Отладочная информация
    # Фильтрация результатов по порогу расстояния (distance_threshold)
    filtered_results = [
        (doc, metadata, dist) for doc, metadata, dist in zip(results['documents'][0], results['metadatas'][0], results['distances'][0]) if dist <= distance_threshold
    ]

    # Проверка наличия релевантных результатов
    if not filtered_results:
        return "В базе знаний не нашлось необходимой информации.", ""

    # Формирование контекста из отфильтрованных результатов
    context = " ".join([doc for doc, _, _ in filtered_results])

    # Формирование списка метаданных для вывода
    metadata_info = "  \n  ".join([
        f"File: [link]({metadata['filename']}), Page: {metadata.get('page_number', 'N/A')} " 
        for _, metadata, _ in filtered_results if metadata is not None
    ])
    
    mymeta = []
    for _, metadata, _ in filtered_results:
        if metadata is not None:
            mymeta.append( [metadata['filename'], metadata.get('page_number', 'N/A'), 0])
    
    metadata_info = mymeta

    prompt = PROMPT_TEMPLATE.format(context=context, question=question)  # Подстановка контекста и вопроса в шаблон
    return prompt, metadata_info

       



# -----------------------------------------------------------------------------
# --                        Секция генерации ответов                         --
# -----------------------------------------------------------------------------

def getRAGAnswer(model, question, collection, SentenceModel, temperature, number_results, distance ):
    logging.info(f"Question: {question}.")

    prompt, metadata_info = search_and_generate_rag_prompt(question, collection, SentenceModel, distance, number_results)
    logging.info(f"Prompt: {prompt}.")

    if "В базе знаний не нашлось необходимой информации." in prompt:
        return prompt, ""
    else:
    # Отправка промпта модели и получение ответа
        completion  =  model.create_chat_completion(
            messages=[ {"role": "user", "content": prompt} ],
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            repeat_penalty=repeat_penalty,
            stream=False)
        response = completion['choices'][0]['message']['content']
        logging.info(f"{response}Источники информации:{metadata_info}")

        return response, metadata_info
    

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
logging.info("Старт")



# -----------------------------------------------------------------------------
# --                        Секция генерации ответов                         --
# -----------------------------------------------------------------------------

def getFreeAnswer(model, question, prompt_template, temperature):
    logging.info(f"Question: {question}.")
    print (prompt_template)


    prompt = prompt_template.format(question=question)  # Подстановка контекста и вопроса в шаблон
 
    logging.info(f"Prompt:{prompt}")
    completion  =  model.create_chat_completion(
            messages=[ {"role": "user", "content": prompt} ],
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            repeat_penalty=repeat_penalty,
            stream=False)
    response = completion['choices'][0]['message']['content']
    logging.info(f"{response}")

    return response
    