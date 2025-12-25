from langchain_groq import ChatGroq
from dotenv import load_dotenv
import streamlit as st
from langchain_classic.prompts import ChatPromptTemplate
from langchain_classic.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

load_dotenv()


def colored_box(
    text,
    bg_color="#EEE",
    text_color="#000",
    align="left",        # "left", "center", "right"
    width="fit-content"  # or "100%", "60%", etc.
):
    align_map = {
        "left": "flex-start",
        "center": "center",
        "right": "flex-end"
    }

    
    return    f"""
        <div style="display:flex; justify-content:{align_map.get(align, 'flex-start')};">
            <div style="
                background-color:{bg_color};
                padding:15px;
                border-radius:8px;
                color:{text_color};
                font-weight:500;
                width:{width};
            ">
                {text}
            </div>
        </div>
        """
    
st.markdown("""
<style>
/* Prevent chat messages from hiding behind input */
.block-container {
    padding-bottom: 160px;
}

/* Fix the form to viewport bottom */
div[data-testid="stForm"] {
    position: fixed;
    bottom: 0;
    height : 15%;
    left: 20%;
    width: 60%;
    background: white;
    border-top: 1px solid #ddd;
    padding: 12px 20px;
    z-index: 10000;
}
</style>
""", unsafe_allow_html=True)





config= {"configurable": {"session_id": "abcd"}}

def load_chat_history(session_id: str)-> BaseChatMessageHistory:
    if session_id not in st.session_state :
        st.session_state[session_id] = ChatMessageHistory()
    return st.session_state[session_id]


llm = init_chat_model(model="groq:openai/gpt-oss-120b")

prompt = ChatPromptTemplate.from_messages(messages=[
("system", "You are a very rude Assistant. You always answer very rudely. There cannot be anyone in this world as rude as you"),
("user", "{input}")
])


main_chain = prompt | llm 

hist_chain = RunnableWithMessageHistory(main_chain, load_chat_history) | StrOutputParser()

st.title("Chat with History")

his = load_chat_history("abcd")

if len(his.messages) !=0 :
    for m in his.messages:
        if m.type == "human" :
           st.markdown(colored_box(m.content, "#CEFAD0","#000000", "right"), unsafe_allow_html=True)
        else :
           st.markdown(colored_box(m.content, "#92B3FF","#000000", "left"), unsafe_allow_html=True)

placeholder_h = st.empty()
placeholder_ai = st.empty()

with st.form("chat_form", clear_on_submit=True):
    m ,l,r = st.columns([10,1,1.5], vertical_alignment="bottom")
    with m:
        msgg = st.text_input("").strip()
    
    with l:
        submitted = st.form_submit_button("Send")
    with r:
        if st.form_submit_button(label="Clear Chat"):
            del st.session_state["abcd"]
            st.rerun()


if submitted and msgg:
    placeholder_h.markdown(colored_box(msgg, "#CEFAD0","#000000", "right"), unsafe_allow_html=True)
    msg = ""
    for m in  hist_chain.stream({"input": msgg}, config= config):
        msg = msg + m
        placeholder_ai.markdown(colored_box(msg, "#92B3FF","#000000", "left"), unsafe_allow_html=True)




        
    



