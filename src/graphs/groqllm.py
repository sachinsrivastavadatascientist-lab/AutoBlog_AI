import os
import sys
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from src.exception import CustomException
from src.logger import logging


class GroqLLM:
    def __init__(self):
        load_dotenv()
        

    def get_llm_model(self):
        try:
            groq_api_key = os.getenv("GROQ_API_KEY")
            selected_groq_model = "llama-3.3-70b-versatile"

            llm = ChatGroq(model=selected_groq_model, api_key=groq_api_key,temperature=0)  
            
        except Exception as e:
            raise CustomException(e,sys) from e
        return llm      