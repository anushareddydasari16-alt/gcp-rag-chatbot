import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_google_community import BigQueryVectorStore

load_dotenv()

project_id = os.getenv("PROJECT")

# Vertex AI embedding model
embedding = VertexAIEmbeddings(
    model_name="text-embedding-005",
    project=project_id,
    location="us-central1",
)

# BigQuery vector store
vector_store = BigQueryVectorStore(
    project_id=project_id,
    dataset_name=os.getenv("DATASET"),
    table_name=os.getenv("TABLE"),
    location=os.getenv("REGION"),
    embedding=embedding,
)

# Gemini model on Vertex AI
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    project=project_id,
    location="us-central1",
    vertexai=True,
)

# Prompt used to generate the answer
prompt = PromptTemplate(
    input_variables=["question", "docs"],
    template="""
You answer questions about Google Cloud certification exams.

Use only the information provided in the documents below.
If the answer is not available in the documents, say:
"I could not find this information in the exam guides."

Documents:
{docs}

Question:
{question}

Answer:
""",
)


def ai_helper(query, exam="Both"):
    source_urls = {
        "Associate Cloud Engineer":
            "https://services.google.com/fh/files/misc/associate_cloud_engineer_exam_guide_english.pdf",

        "Professional Cloud Security Engineer":
            "https://services.google.com/fh/files/misc/professional_cloud_security_engineer_exam_guide_english.pdf",
    }

    # Retrieve relevant documents from BigQuery.
    # A larger number is used because exam filtering is done locally.
    documents = vector_store.similarity_search(query, k=20)

    # Filter documents locally based on the selected exam.
    # This avoids the BigQuery metadata filter error.
    if exam != "Both":
        documents = [
            document
            for document in documents
            if document.metadata.get("source") == source_urls[exam]
        ]

    if not documents:
        return (
            "I could not find relevant information in the selected exam guide.",
            [],
        )

    # Combine retrieved document text
    context = "\n\n".join(
        document.page_content for document in documents
    )

    # Create and run the LangChain chain
    chain = prompt | llm

    response = chain.invoke(
        {
            "question": query,
            "docs": context,
        }
    )

    return response.content, documents