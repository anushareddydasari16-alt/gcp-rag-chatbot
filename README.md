
# Google Cloud Certifications Chatbot

A document question-answering chatbot for the Google Cloud Associate Cloud Engineer and Professional Cloud Security Engineer exam guides.

The application uses Streamlit for the interface, Vertex AI for embeddings and Gemini responses, BigQuery for vector storage, and LangChain to connect the components.

## Features

- Select an exam guide or search both guides.
- Ask questions about certification topics.
- Retrieve relevant text from PDF exam guides.
- Generate answers using Gemini on Vertex AI.
- Store document embeddings in BigQuery.
- Display retrieved document pages and source links.
- Respond when information is not available in the indexed documents.

## Architecture

The application follows this workflow:

```text
Exam Guide PDFs
       ↓
PDF Text Extraction
       ↓
Text Cleaning and Chunking
       ↓
Vertex AI Embeddings
       ↓
BigQuery Vector Store
       ↓
Similarity Search
       ↓
Gemini on Vertex AI
       ↓
Streamlit Chatbot
```

## Technologies

| Technology | Purpose |
| --- | --- |
| Python 3.11 | Application development |
| Streamlit | Web interface |
| LangChain | Prompting and retrieval workflow |
| Vertex AI | Embeddings and Gemini responses |
| BigQuery | Vector storage |
| PyPDF | PDF text extraction |
| Conda | Python environment management |

## Project files

| File | Purpose |
| --- | --- |
| `app.py` | Streamlit chatbot interface |
| `ai.py` | Retrieval and Gemini response logic |
| `knowledge_base.py` | Downloads, processes, and indexes the PDFs |
| `requirements.txt` | Python dependencies |
| `.env.example` | Configuration template |
| `.gitignore` | Prevents credentials and local files from being uploaded |
| `PROJECT_REPORT.md` | Project explanation and testing report |
| `LICENSE` | Project license |
| `images/architecture.png` | System architecture diagram |

## Google Cloud setup

Create a Google Cloud project and enable:

- Vertex AI API
- BigQuery API

Create a BigQuery dataset named:

```text
rag_chatbot
```

Use the `US` multi-region for the BigQuery dataset.

## Local setup on Windows

Create and activate the Conda environment:

```powershell
conda create -n gemini-rag python=3.11 -y
conda activate gemini-rag
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
python -m pip install langchain-community langchain-text-splitters python-dotenv pypdf
```

Authenticate with Google Cloud:

```powershell
gcloud init
gcloud config set project YOUR_PROJECT_ID
gcloud auth application-default login
gcloud auth application-default set-quota-project YOUR_PROJECT_ID
```

Replace `YOUR_PROJECT_ID` with your Google Cloud project ID.

## Environment configuration

Create a file named `.env` in the project folder:

```env
PROJECT=YOUR_PROJECT_ID
DATASET=rag_chatbot
TABLE=certification_documents_clean
REGION=US
```

Replace `YOUR_PROJECT_ID` with your own project ID.

Do not upload `.env` to GitHub.

## Load the exam guides

Run:

```powershell
python knowledge_base.py
```

This downloads the exam guide PDFs, extracts the text, cleans the content, creates chunks, generates embeddings, and stores the documents in BigQuery.

Run the ingestion script once for a fresh table. Running it repeatedly on the same table can create duplicate records.

## Run the chatbot

Start Streamlit:

```powershell
python -m streamlit run app.py
```

Open the local URL shown in the terminal. Select an exam guide, enter a question, and click **Ask**.

Example questions:

```text
What are the main sections of the Professional Cloud Security Engineer exam?

What does Section 3 of the security exam cover?

What topics are included in the Associate Cloud Engineer exam?

What is the exam registration fee?
```

If the requested information is not included in the exam guides, the chatbot is instructed to say that it could not find the information.

## Testing completed

- Loaded both exam guide PDFs successfully.
- Created document chunks and stored embeddings in BigQuery.
- Tested questions about both certification exams.
- Tested exam-specific filtering.
- Verified that retrieved page numbers and source links appear in the application.
- Tested a question whose answer was not available in the documents.
- Improved text extraction by cleaning excessive PDF whitespace.

## Limitations

- The application uses only two exam guides.
- It does not perform live web searches.
- It does not include chat history.
- It is intended for local use.
- It does not include user login or access control.
- The ingestion script can create duplicates if run repeatedly on the same table.
- Retrieved pages are supporting context, not guaranteed claim-level citations.
- Package deprecation warnings may require future updates.

## Useful documentation

- [Google Cloud Vertex AI](https://cloud.google.com/vertex-ai)
- [Google BigQuery](https://cloud.google.com/bigquery)
- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [Associate Cloud Engineer exam guide](https://services.google.com/fh/files/misc/associate_cloud_engineer_exam_guide_english.pdf)
- [Professional Cloud Security Engineer exam guide](https://services.google.com/fh/files/misc/professional_cloud_security_engineer_exam_guide_english.pdf)
```