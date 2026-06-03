import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq


class GroqLLM:
    def __init__(self):
        load_dotenv()
        

    def get_llm_model(self):
        try:
            groq_api_key = os.getenv("GROQ_API_KEY")
            selected_groq_model = "llama-3.3-70b-versatile"

            llm = ChatGroq(model=selected_groq_model, api_key=groq_api_key)  
            
        except Exception as e:
            raise ValueError(f"Error Occured in groqllm module Wih Exception : {e}")

        return llm      