# 🔗 Smart URL Answer Bot

A Retrieval-Augmented Generation (RAG) app that lets you ask questions about the content of any web page. Paste in up to three URLs, and the app scrapes, chunks, and embeds the content into a vector database — then answers your questions using an LLM, citing the sources it pulled from.

Built with **Streamlit**, **LangChain**, **Groq**, **HuggingFace embeddings**, and **ChromaDB**.

## ✨ Features

- 📥 Process up to 3 URLs at a time
- ✂️ Automatic text chunking for efficient retrieval
- 🧠 Semantic search powered by HuggingFace embeddings
- 💬 Fast LLM-generated answers via Groq (Llama 3.3 70B)
- 📚 Source attribution for every answer
- 🗄️ Persistent local vector store (Chroma)

## 🛠️ Tech Stack

| Component | Tool |
|---|---|
| UI | [Streamlit](https://streamlit.io/) |
| Orchestration | [LangChain](https://www.langchain.com/) |
| LLM | [Groq](https://groq.com/) — `llama-3.3-70b-versatile` |
| Embeddings | HuggingFace — `Alibaba-NLP/gte-base-en-v1.5` |
| Vector Store | [ChromaDB](https://www.trychroma.com/) |
| Web Scraping | LangChain `UnstructuredURLLoader` |

## 🧩 How It Works

1. **Process URLs** — The app loads and scrapes the given URLs, splits the text into chunks, embeds them, and stores them in a local Chroma vector store (the collection is reset each time you process new URLs).
2. **Ask a Question** — Your query is embedded and used to retrieve the most relevant chunks from the vector store.
3. **Generate Answer** — The retrieved chunks are passed to the Groq LLM via a `RetrievalQAWithSourcesChain`, which returns an answer along with the source URLs it used.

## 📋 Prerequisites

- Python 3.10+
- A [Groq API key](https://console.groq.com/keys)
- A [Hugging Face access token](https://huggingface.co/settings/tokens)

## 🚀 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>
   ```

2. **Create and activate a virtual environment** (recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the project root:

   ```env
   GROQ_API_KEY=your_groq_api_key_here
   HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
   ```

## ▶️ Usage

Run the Streamlit app:

```bash
streamlit run main_rag.py
```

Then in the app:

1. Enter one to three URLs in the sidebar and click **🚀 Process URLs**.
2. Wait for the status messages to confirm processing is complete.
3. Type a question in the main panel and press Enter.
4. View the generated answer and its source links.

> ⚠️ You must process at least one URL before asking a question, or you'll see a warning prompting you to do so.

## 📁 Project Structure

```
.
├── main_rag.py          # Streamlit frontend (UI, input handling)
├── rag.py                # RAG pipeline (scraping, embedding, retrieval, answering)
├── requirements.txt      # Python dependencies
└── resources/
    └── vector_store/      # Persisted Chroma vector store (created at runtime)
```

## ⚙️ Configuration

A few values can be tuned directly in `rag.py`:

| Variable | Default | Description |
|---|---|---|
| `CHUNK_SIZE` | `1000` | Max characters per text chunk |
| `EMBEDDING_MODEL` | `Alibaba-NLP/gte-base-en-v1.5` | HuggingFace embedding model |
| `COLLECTION_NAME` | `real_estate` | Chroma collection name |
| LLM model | `llama-3.3-70b-versatile` | Groq model used for answer generation |
| LLM temperature | `0.9` | Controls answer creativity/randomness |

## 📝 Notes & Limitations

- Processing new URLs **resets** the existing vector store collection — previously indexed content is cleared each time.
- Answer quality depends on how well `UnstructuredURLLoader` can parse a given page (JS-heavy or paywalled sites may not scrape well).
- The vector store is stored locally in `resources/vector_store/` and is not included in version control by default — add it to `.gitignore`.

## 📄 License

Add your preferred license here (e.g., MIT, Apache 2.0).
