# Streamlit RAG Chatbot

A simple Retrieval-Augmented Generation (RAG) chatbot powered by Streamlit. This project demonstrates how to build an interactive chatbot interface using Streamlit, enabling users to ask questions and receive context-aware answers based on retrieval from a knowledge source.

## Features

- **Streamlit UI**: Easy-to-use web interface for chatting.
- **RAG Pipeline**: Integrates retrieval and generation for more accurate answers.
- **Customizable Knowledge Base**: Easily swap out or update the data source.
- **OpenAI API Integration** (if configured): Use LLMs for generating answers.
- **Local and Cloud Support**: Run locally or deploy on Streamlit Cloud.

## Live Demo

Try the chatbot online:  
👉 [https://app-rag-chatbot.streamlit.app/](https://app-rag-chatbot.streamlit.app/)

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Sumit-1018/streamlit-rag-chatbot.git
    cd streamlit-rag-chatbot
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **(Optional) Set up API keys:**
   - If using OpenAI or other APIs, create a `.env` file or set environment variables as needed.

### Running the App Locally

```bash
streamlit run app.py
```

Open your browser and go to [http://localhost:8501](http://localhost:8501).

## Usage

- Enter your question in the chat input.
- The chatbot retrieves relevant context and generates an answer.
- Review source/context snippets for transparency.

## Project Structure

```
├── app.py                # Main Streamlit application
├── rag_pipeline.py       # RAG pipeline logic
├── requirements.txt      # Python dependencies
├── data/                 # Example or default knowledge base
├── README.md             # Project documentation
```

## Customization

- **Knowledge Base**: Replace or extend files in the `data/` directory.
- **RAG Logic**: Modify `rag_pipeline.py` to change retrieval or generation strategies.
- **UI**: Adjust `app.py` for new features or layout tweaks.

## Contributing

Pull requests and suggestions are welcome! Please fork the repository and submit your changes via a pull request.

## License

This project is licensed under the MIT License.

## Author

**Sumit Gupta**

- GitHub: [Sumit-1018](https://github.com/Sumit-1018)
- LinkedIn: [sumitgupta1018](https://www.linkedin.com/in/sumitgupta1018/)

---
