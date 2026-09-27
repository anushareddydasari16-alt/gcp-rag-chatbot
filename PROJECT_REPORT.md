
# Google Cloud Certifications Chatbot
## Project Report

**Author:** Anusha Reddy Dasari  
**Project type:** Personal learning project  
**Date:** September 2026

## 1. Project overview

I developed a Google Cloud certifications chatbot to understand how a retrieval-augmented generation application works with Vertex AI, BigQuery, LangChain, and Streamlit.

The chatbot answers questions about the Associate Cloud Engineer and Professional Cloud Security Engineer exam guides. Users can select a specific exam or search both guides. The application retrieves relevant document sections and sends them to Gemini to generate an answer.

The goal of this project was to build an end-to-end machine learning application that includes document processing, embeddings, vector search, prompt design, and a simple user interface.

## 2. Project objectives

The main objectives were:

- Load public Google Cloud certification exam guides.
- Extract and clean text from PDF files.
- Split documents into smaller searchable chunks.
- Generate embeddings using Vertex AI.
- Store text, embeddings, and metadata in BigQuery.
- Retrieve relevant information using vector similarity search.
- Generate answers using Gemini.
- Display the answer and related document pages in Streamlit.

## 3. System design

The system has two main workflows.

### Document ingestion

The `knowledge_base.py` script downloads and processes the exam guides.

The workflow is:

1. Download the PDF files.
2. Extract text page by page.
3. Clean unnecessary spaces and line breaks.
4. Split the text into chunks.
5. Add source and page metadata.
6. Generate embeddings with Vertex AI.
7. Store the text and embeddings in BigQuery.

The text splitter uses a chunk size of 2,000 characters and an overlap of 200 characters.

### Question answering

The user selects an exam guide and enters a question.

The application then:

1. Converts the question into an embedding.
2. Searches BigQuery for similar document chunks.
3. Filters results when a specific exam is selected.
4. Sends the retrieved text and question to Gemini.
5. Displays the generated answer.
6. Shows the retrieved PDF pages as supporting sources.

## 4. Google Cloud services

I used the following Google Cloud services:

- Vertex AI for document embeddings and Gemini responses.
- BigQuery for storing document chunks, metadata, and vectors.
- Application Default Credentials for local authentication.
- Google Cloud project configuration for service access and quota management.

The BigQuery dataset uses the `US` multi-region. Vertex AI requests use the `us-central1` region.

## 5. Important implementation decisions

I cleaned the extracted PDF text before splitting it into chunks:

```python
page.page_content = " ".join(page.page_content.split())
```

This was necessary because some PDF text was extracted with excessive line breaks and spaces. Cleaning the text made the sections easier to retrieve.

I also added an exam selector. When the user chooses one exam, the application filters retrieval using the document source URL. This reduces unrelated context from the other exam guide.

The prompt instructs Gemini to answer using the retrieved documents and to say when the requested information cannot be found.

## 6. Testing and results

I performed manual tests during development.

| Test | Result |
| --- | --- |
| PDF download | Successful |
| Text extraction | Successful |
| BigQuery table creation | Successful |
| Embedding generation | Successful |
| Question about the Associate exam | Returned relevant topics |
| Question about the Security exam | Returned relevant sections |
| Exam-specific filtering | Returned the selected exam guide |
| Source page display | Displayed retrieved page links |
| Missing registration-fee question | Reported that the information was not found |

During testing, one question about the security exam initially missed Section 3. I inspected the extracted text and found that the PDF formatting had separated many words with whitespace. After cleaning the text and rebuilding the embeddings, the answer included all five exam sections.

The five security exam sections were retrieved as:

- Configuring access
- Securing communications and establishing boundary protection
- Ensuring data protection
- Managing operations
- Supporting compliance requirements

## 7. Challenges and solutions

### PDF text formatting

The extracted PDF text did not always preserve normal spacing. I solved this by normalizing whitespace before creating chunks.

### Retrieval scope

Searching both exam guides could return unrelated pages. I added exam-specific filtering to make the retrieved context more relevant.

### Streamlit filename conflict

A local file named `streamlit.py` conflicted with the installed Streamlit package. I renamed the interface file to `app.py` and used:

```python
import streamlit as st
```

### Authentication

The Python application uses Application Default Credentials. This allowed the application to access Vertex AI and BigQuery through the Google Cloud project without placing credentials inside the source code.

## 8. Current limitations

The current application is a working prototype.

It currently has:

- Two indexed exam guides.
- No live web search.
- No conversation memory.
- No user login.
- No public deployment.
- No automatic document refresh.
- No formal accuracy benchmark.
- No claim-level citation verification.
- No monitoring dashboard.
- No duplicate protection during repeated ingestion.

The application also produced deprecation warnings for some LangChain integrations. These warnings did not prevent the application from running, but dependency updates should be reviewed in a future version.

## 9. Future improvements

Future improvements could include:

- Adding more certification guides.
- Preventing duplicate document ingestion.
- Adding automated evaluation questions.
- Measuring retrieval accuracy and response time.
- Adding conversation history.
- Adding stronger citation support.
- Adding document upload functionality.
- Deploying the application to a managed cloud service.
- Adding logging and monitoring.
- Pinning tested package versions.

## 10. Lessons learned

This project helped me understand the complete RAG workflow from document ingestion to user response.

I learned that document quality affects retrieval quality. Increasing the number of retrieved chunks did not solve the missing section until I inspected and cleaned the extracted text.

I also learned how embeddings and vector search connect documents to user questions. BigQuery stores the searchable content, while Vertex AI provides the embedding and language model capabilities.

The project improved my understanding of cloud authentication, environment configuration, prompt design, metadata filtering, and Streamlit application development.
```