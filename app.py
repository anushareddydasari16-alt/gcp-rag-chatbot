import streamlit as st
from ai import ai_helper

st.title("Google Cloud Certifications Chatbot")
st.write(
    "Ask questions about the Associate Cloud Engineer and "
    "Professional Cloud Security Engineer exam guides."
)

with st.form("question_form"):
    exam = st.selectbox(
        "Choose an exam guide",
        [
            "Both",
            "Associate Cloud Engineer",
            "Professional Cloud Security Engineer",
        ],
    )

    question = st.text_input("What would you like to know?")
    submitted = st.form_submit_button("Ask")

if submitted:
    if not question.strip():
        st.info("Please enter a question.")
    else:
        with st.spinner("Searching the exam guides..."):
            answer, documents = ai_helper(question, exam)

        st.markdown(answer)

        if documents:
            with st.expander("View retrieved sources"):
                st.caption(
                    "These pages were provided to the model as context. "
                    "They are not verified citations for every statement."
                )

                shown_sources = set()

                for document in documents:
                    url = document.metadata.get("source", "")
                    page = document.metadata.get("page")

                    if not url:
                        continue

                    source_id = (url, page)

                    if source_id in shown_sources:
                        continue

                    shown_sources.add(source_id)

                    name = url.rsplit("/", 1)[-1].replace("_", " ")

                    if page is not None:
                        page_number = int(page) + 1
                        st.markdown(
                            f"- [{name} — page {page_number}]"
                            f"({url}#page={page_number})"
                        )
                    else:
                        st.markdown(f"- [{name}]({url})")