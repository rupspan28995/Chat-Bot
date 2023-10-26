import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import FAISS 
from langchain.chains import ConversationalRetrievalChain
#from htmltemplates import css, bot_template, user_template

# import os
# import openai
css= '''
<style>
.chat-message {
      padding : 1.5rem; border-radius: 0.5rem, margin-bottom:1rem; display: flex
}
.chat-message.user {
      background-color: #2b313e
}
.chat-message.bot {
      background-color: #475063
}
.chat-message .avatar {
      width: 15%;
}
.chat-message .avatar img {
      max -width: 78px;
      max-height: 78px;
      border-radius: 50%;
      object-fit: cover;
}
.chat-message .message {
      width: 85%;
      padding: 0 1.5rem;
      color: #fff
}
'''
bot_template='''
<div class="chat-message bot">
  <div class= "avatar">
     <img src="https://ozonetel.com/wp-content/uploads/2021/02/voicebot.jpg" style="max-height: 78px; max-width: 78px; border-radius: 50%">
  </div>
  <div class="message">{{MSG}}</div>
</div>
'''
user_template='''
<div class="chat-message user">
  <div class= "avatar">
     <img src="https://cdn.vox-cdn.com/thumbor/pgFEqJ5ZUTt3tyOBKTTg3YN26ek=/0x0:1080x718/920x613/filters:focal(477x288:649x460):format(webp)/cdn.vox-cdn.com/uploads/chorus_image/image/71263353/300017093_10114630004939621_5854109382330704814_n.0.jpg" >
  </div>
  <div class="message">{{MSG}}</div>
</div>
'''
# openai.organization = "org-iBolOnEZ0KYyOA6e5bGK41cd"
# openai.api_key = os.getenv("OPENAI_API_KEY")

# from streamlit_extras.add_vertical_space import add_vertical_space

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
       pdf_reader= PdfReader(pdf)
       for page in pdf_reader.pages:
           text += page.extract_text()
    return text
    
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap = 300
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts= text_chunks, embedding = embeddings)
    vectorstore.save_local("faiss_vectorstore")
    return vectorstore

def get_conversation_chain(vectorstore):
    llm= ChatOpenAI()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever=vectorstore.as_retriever(),
        memory= memory
    )
    return conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}",message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}",message.content), unsafe_allow_html=True)
def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with Multiple PDFs", page_icon=":books:")

    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    
    st.header("Chat with IPAN Bot :books:") #Header of the chat bot
    user_question= st.text_input("Ask a question")

    if user_question:
        handle_userinput(user_question)


    with st.sidebar:
        st.subheader("Your Documents")
        pdf_docs= st.file_uploader("Upload", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
               # get pdf text
               print("raw_text here")
               raw_text= get_pdf_text(pdf_docs)
               print(raw_text)

               # get the text chunks
               text_chunks = get_text_chunks(raw_text)
               print("text_chunks here")
               print(text_chunks)
               st.write(text_chunks)
               print("text_chunks finished")
               # create vector store 
               vectorstore = get_vectorstore(text_chunks)

               # create conversation chain
               st.session_state.conversation = get_conversation_chain(vectorstore)
    

         
if __name__  == '__main__':
    main()