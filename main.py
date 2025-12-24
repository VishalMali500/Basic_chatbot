from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import streamlit as st
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model = "openai/gpt-oss-120b" , api_key=groq_api_key)

msg = st.text_input("What you want ?")

if st.button("Send") : 
    st.write(llm.invoke(msg).content)


