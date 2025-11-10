import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Semantic Search & RAG", layout="wide")

st.title("🔎 Semantic Search + Local RAG (Phi-3)")

tabs = st.tabs(["Search", "Ask a Question", "Chat", "Upload Documents"])


# ---------------- SEARCH TAB -----------------
with tabs[0]:
    st.subheader("Semantic Search")
    query = st.text_input("Enter search query")

    if st.button("Search"):
        if query.strip():
            response = requests.get(f"{API_URL}/search", params={"q": query})
            results = response.json()["results"]

            for r in results:
                st.markdown(f"### {r['title']}")
                st.write(f"**Score:** {round(r['score'], 4)}")
                st.write(r["content"])
                st.markdown("---")


# ---------------- RAG ANSWER TAB -----------------
with tabs[1]:
    st.subheader("Ask a Question (RAG using Phi-3)")
    question = st.text_input("Enter your question")

    if st.button("Ask"):
        if question.strip():
            response = requests.post(f"{API_URL}/answer", json={"question": question})
            # answer = response.json()["answer"]
            # st.markdown("### 🧠 Answer")
            # st.write(answer)
            response_json = response.json()

            st.markdown("### 🧠 Answer")
            st.write(response_json["answer"])

            st.markdown("### 📚 Sources Used")
            for i, chunk in enumerate(response_json["chunks"]):
                with st.expander(f"Source Chunk {i}"):
                    st.write(chunk["content"])

# ---------------- RAG CHAT TAB -----------------
with tabs[2]:
    st.subheader("Ask Questions (Chat Mode)")

    # Store chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display existing messages
    for role, message in st.session_state.chat_history:
        if role == "user":
            st.markdown(f"""
            <div style="text-align: right; background-color: #121212; padding: 8px; border-radius: 8px; margin-bottom: 6px;">
                {message}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="text-align: left; background-color: #121212; padding: 8px; border-radius: 8px; margin-bottom: 6px;">
                {message}
            </div>
            """, unsafe_allow_html=True)

    # User input box at bottom
    question = st.text_input("Type your question here:")

    if st.button("Send"):
        if question.strip():
            # Add user message
            st.session_state.chat_history.append(("user", question))

            # Call backend
            response = requests.post(f"{API_URL}/answer", json={"question": question})
            response_json = response.json()

            # Add model reply to chat history
            st.session_state.chat_history.append(("assistant", response_json["answer"]))

            # Display sources
            st.markdown("### 📚 Sources Used")
            for i, chunk in enumerate(response_json["chunks"]):
                with st.expander(f"Source {i}"):
                    st.write(chunk["content"])

            # Clear text field
            st.rerun()

# ---------------- UPLOAD TAB -----------------
with tabs[3]:
    st.subheader("Upload a PDF or Text File")

    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt"])

    if uploaded_file:
        # Save file to documents folder
        save_path = f"documents/{uploaded_file.name}"
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"✅ Saved to {save_path}")

        # Show a button to process
        if st.button("Process & Ingest"):
            # Call FastAPI ingestion endpoint
            resp = requests.post(f"{API_URL}/ingest_file", json={"path": save_path})
            st.write(resp.json())


