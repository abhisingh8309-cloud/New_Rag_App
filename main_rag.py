import streamlit as st 
from rag import generate_answer, process_urls

# Set page configuration
st.set_page_config(page_title="Smart URL Answer Bot", page_icon="🔗",layout="centered")

# App Title
st.title("🔗 Your Smart URL Answer Bot")
st.markdown("Ask question based on content from your favorite web pages.")

# Sidebar - URL Input Section 
st.sidebar.header("📥Enter URLS to Process")
url1 = st.sidebar.text_input(' URL 1')
url2 = st.sidebar.text_input(' URL 2')
url3 = st.sidebar.text_input(' URL 3')

# Placeholder for the status message
status_placeholder = st.empty()

# Button to process URLS 
if st.sidebar.button('🚀 Process URLs'):
    urls = [url for url in (url1, url2, url3) if url.strip() != '']
    if not urls:
        status_placeholder.error("⚠️ Please enter at least one valid URL.")
    else:
        for status in process_urls(urls):
            status_placeholder.info(status)

# Divider 
st.markdown("---")

# Main Input - Question
st.subheader("💭 Ask a Question")
query = st.text_input("Type yours question here and press Enter:")

# show answer if query is submited

if query:
    try:
        answer, sources = generate_answer(query)
        st.success("✅ Answer Generated!")

        st.markdown("### 🧠 Answer")
        st.write(answer)

        if sources:
            st.markdown("### 📚 Sources")
            for sources in sources.strip().split("\n"):
                if sources.strip():
                    st.markdown(f"- {sources}")
    except RuntimeError:
        st.error("⚠️ You must process the URLS first before asking a question.")