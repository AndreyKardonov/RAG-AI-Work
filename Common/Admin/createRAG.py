import streamlit as st 
import json
import os
from sentence_transformers import SentenceTransformer
import chromadb
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader

import torch as torch

# Функция для получения полного пути до всех файлов в каталоге, включая подкаталоги
def get_file_names(root_dir):
    listfiles = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            listfiles.append(os.path.join(root, file))
           # print(os.path.join(root, file))
    return listfiles


#########################################
# Функция для разбивки текста на куски (chunks) заданного размера с перекрытием
def chunk_text_with_overlap(text, chunk_size, chunk_overlap):
    words = text.split()
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        yield ' '.join(words[start:end])
        start += chunk_size - chunk_overlap


#########################################
 

#  для извлечения текста и номеров страниц
def extract_text(type, path):
    if(type=="pdf"):
        loader = PyPDFLoader(path)
    if(type=="md"):
        loader = TextLoader(path, "UTF-8")
    if(type=="doc" or type=="docx"):
        loader = UnstructuredWordDocumentLoader(path)

    documents = loader.load()
    text = []
    page_numbers = []
    for i, doc in enumerate(documents):
        text.append(doc.page_content)
        # Добавляем номер страницы (i+1, так как нумерация страниц начинается с 1)
        page_numbers.extend([i+1] * len(doc.page_content.split()))  # Каждое слово получает номер страницы
    return " ".join(text), page_numbers


#########################################


def get_chunks(listfiles, mySentenceModel):

    chunk_size = 300  # 200   # Задание размера chunks
    chunk_overlap = 30  # 20   # Задание перекрытия chunks (20 слов)
    documents = []  # Список для хранения текстовых кусков
    ids = []  # Список для хранения уникальных идентификаторов кусков
    metadata = []  # Список для хранения метаданных
    total_chunks = 0  # Переменная для подсчета общего количества чанков
    total_documents = 0  # Переменная для подсчета общего количества документов
    embeddings = []

    # Проход по всем файлам в указанной папке 
    for filename in listfiles:
        extension=filename.split('.')[-1].lower()
        if extension=="md" or extension=="pdf" or extension=="doc" or extension=="docx" : # Проверка, что файл имеет расширение .md

            print(f"  Filename: {filename}") # Выводим название обрабатываемого файла
            file_path = filename#os.path.join(folder_path, filename)
#            content, page_numbers = extract_text_from_md(file_path)  # Извлечение текста и номеров страниц из PDF файла

            content, page_numbers =  extract_text(extension, file_path)


            chunks = list(chunk_text_with_overlap(content, chunk_size, chunk_overlap))  # Разбивка текста на chunks          
            total_chunks += len(chunks)  # Увеличение общего количества чанков
            total_documents += 1  # Увеличение общего количества документов
            for i, chunk in enumerate(chunks):
                documents.append(chunk)  # Добавление текстового куска
                ids.append(f"{filename}_chunk_{i}")  # Создание уникального идентификатора для каждого куска
            
                embeddings.append(mySentenceModel.encode(chunk).tolist())  # Векторизация чанка и преобразование в список
                
                # Определение номера страницы для текущего чанка
                chunk_words = chunk.split()
                chunk_page_numbers = [page_numbers[j] for j in range(i * (chunk_size - chunk_overlap), i * (chunk_size - chunk_overlap) + len(chunk_words))]
                page_number = max(set(chunk_page_numbers), key=chunk_page_numbers.count)  # Определение самой часто встречающейся страницы в чанке
                metadata.append({"filename": filename, "chunk_id": f"{filename}_chunk_{i}", "page_number": page_number})  # Добавление метаданных
            #  print(f"  Page_number: {page_number}") # Выводим номер обрабатываемой страницы
                
    print (f"Total chunks = {total_chunks}")
    return embeddings, metadata, documents, ids,total_chunks, total_documents


#########################################


def createRAG(baseName, docpath, ragpath, sentencer, sentencer_path, collection_name, chuncker):

    fullpath = docpath
    DB_path = ragpath  # Путь к векторной базе данных
    collection_name  = collection_name  # Имя коллекции
    SentenceModelPath = sentencer_path # локальный путь для модели эмбедера

    # Создание клиента Chroma для работы с постоянным хранилищем (PersistentClient).
    chroma_client = chromadb.PersistentClient(path=DB_path)
    try:
        chroma_client.delete_collection(collection_name) 
    except:
        print('Коллекции нет, ну и ничего страшного.')
    
    # Получение или создание коллекции
    collection_md = chroma_client.get_or_create_collection(name=collection_name) 
    mySentenceModel = SentenceTransformer(SentenceModelPath) # Инициализация модели для word embeddings

    listfiles = get_file_names(fullpath)
    embeddings , metadata, documents, ids, total_chunks, total_documents = get_chunks(listfiles, mySentenceModel)
 

    collection_md.upsert(
        embeddings=embeddings,
        documents=documents,
        ids=ids,
        metadatas=metadata
    )
    import gc
 
    torch.cuda.empty_cache()
    # Вывод сообщения о количестве документов и чанков

    st.session_state.settings["RAGBases"][baseName] = {
        "Sentencer":sentencer,
        "DBPath":ragpath,
        "DOCPath":docpath,
        "CollectionName":collection_name,
        "Chuncker":chuncker
          }
     
    with open(st.session_state.settings_file, 'w') as f:
        json.dump(st.session_state.settings, f)


    print(f"Разбили документов - {total_documents} на {total_chunks} чанков.")

    return f"Разбили документов - {total_documents} на {total_chunks} чанков."

 