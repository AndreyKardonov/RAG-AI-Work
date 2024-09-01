import streamlit as st 
import torch
from llama_cpp import Llama


@st.cache_resource
def initModel(model_full_path):             # 
    model = Llama(
        model_path=model_full_path,
        n_ctx=20000,
        n_gpu_layers=-1, n_threads=32, n_batch=1024, 
        n_parts=1,
        verbose=False,
       )
    return model


def reLoadModel(model, model_full_path):             # 
    if model== "":
        return ""
    else:
        model.close()
        torch.cuda.empty_cache()       
        model = Llama(
            model_path=model_full_path,
            n_ctx=20000,
            n_gpu_layers=-1, n_threads=32, n_batch=1024, 
            n_parts=1,
            verbose=False,
           )
    return model


def freeModel(model):             # 
    if model!= "":
        model.close()
        torch.cuda.empty_cache()   
    return ""