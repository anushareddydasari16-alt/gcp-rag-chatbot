import os
from pathlib import Path
from urllib.request import urlretrieve

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_google_community import BigQueryVectorStore

load_dotenv()

project_id = os.getenv("PROJECT")

# Download the certification guides into a local folder.
data_folder = Path(__file__).parent / "data"
data_folder.mkdir(exist_ok=True)

urls = [
    "https://services.google.com/fh/files/misc/associate_cloud_engineer_exam_guide_english.pdf",
    "https://services.google.com/fh/files/misc/professional_cloud_security_engineer_exam_guide_english.pdf",
]

documents = []

for url in urls:
    file_path = data_folder / url.split("/")[-1]

    if not file_path.exists():
        print(f"Downloading {file_path.name}")
        urlretrieve(url, file_path)

    pages = PyPDFLoader(str(file_path)).load()

    for page in pages:
        page.page_content = " ".join(page.page_content.split())
        page.metadata["source"] = url

    documents.extend(pages)

# Split the PDF pages into smaller pieces.
splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=200,
)

chunks = splitter.split_documents(documents)
chunks = [chunk for chunk in chunks if chunk.page_content.strip()]

if not chunks:
    raise ValueError("No text was extracted from the PDFs.")

for index, chunk in enumerate(chunks):
    chunk.metadata["chunk"] = index

print(f"Loaded {len(documents)} pages and created {len(chunks)} chunks.")

# Use Vertex AI to convert text into embeddings.
embedding = VertexAIEmbeddings(
    model_name="text-embedding-005",
    project=project_id,
    location="us-central1",
)

# Store the text and embeddings in BigQuery.
vector_store = BigQueryVectorStore(
    project_id=project_id,
    dataset_name=os.getenv("DATASET"),
    table_name=os.getenv("TABLE"),
    location=os.getenv("REGION"),
    embedding=embedding,
)

vector_store.add_documents(chunks)

print("Documents and embeddings saved to BigQuery.")