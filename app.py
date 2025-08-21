import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
# NEW: Import the correct chain for conversations
from langchain.chains import ConversationalRetrievalChain

# Load environment variables from .env file
load_dotenv()

def main():
    """
    Main function to run the Streamlit application.
    """
    st.set_page_config(page_title="Chat with Your PDF 📄", layout="wide")
    st.title("Chat with Your PDF using Google Gemini 🤖")
    
    # --- Sidebar for PDF Upload ---
    with st.sidebar:
        st.header("Your Document")
        pdf_file = st.file_uploader("Upload your PDF here and click 'Process'", type="pdf")
        
        if st.button("Process"):
            if pdf_file is not None:
                with st.spinner("Processing PDF... Please wait."):
                    try:
                        # Save the uploaded file temporarily
                        with open(pdf_file.name, "wb") as f:
                            f.write(pdf_file.getbuffer())
                        
                        loader = PyPDFLoader(pdf_file.name)
                        documents = loader.load()
                        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
                        chunks = text_splitter.split_documents(documents)
                        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
                        vector_store = FAISS.from_documents(chunks, embeddings)
                        
                        # Save the vector store and retriever in session state
                        st.session_state.vector_store = vector_store
                        st.session_state.retriever = vector_store.as_retriever()
                        
                        # Initialize chat history
                        st.session_state.messages = [
                            {"role": "assistant", "content": f"PDF '{pdf_file.name}' processed! How can I help you?"}
                        ]
                        os.remove(pdf_file.name)
                        st.success("PDF Processed!")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
            else:
                st.warning("Please upload a PDF file first.")
    
    # --- Main Chat Interface ---
    if "messages" not in st.session_state:
        st.info("Please upload a PDF in the sidebar to begin.")
    else:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input
        if prompt := st.chat_input("Ask a question about your document"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        llm = GoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=os.getenv("GOOGLE_API_KEY"))
                        
                        # NEW: Create the ConversationalRetrievalChain
                        conversation_chain = ConversationalRetrievalChain.from_llm(
                            llm=llm,
                            retriever=st.session_state.retriever
                        )

                        # NEW: Format chat history for the chain
                        # The chain expects a list of tuples (human_message, ai_message)
                        chat_history = []
                        for msg in st.session_state.messages:
                           if msg["role"] == "user":
                               chat_history.append((msg["content"], ""))
                           elif msg["role"] == "assistant":
                               if chat_history:
                                   chat_history[-1] = (chat_history[-1][0], msg["content"])
                        
                        # Remove the last user message from history as it's the current question
                        if chat_history and chat_history[-1][1] == "":
                           chat_history = chat_history[:-1]

                        # Invoke the chain with the question and formatted history
                        response_dict = conversation_chain.invoke({
                            "question": prompt,
                            "chat_history": chat_history
                        })
                        
                        # The answer is now in the 'answer' key
                        response = response_dict["answer"]
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})

                    except Exception as e:
                        error_message = f"Failed to get an answer. Error: {e}"
                        st.error(error_message)
                        st.session_state.messages.append({"role": "assistant", "content": error_message})

if __name__ == "__main__":
    main()