import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_google_community import BigQueryVectorStore

load_dotenv()

project_id = os.getenv("PROJECT")

embedding = VertexAIEmbeddings(
    model_name="text-embedding-005",
    project=project_id,
    location="us-central1",
)

vector_store = BigQueryVectorStore(
    project_id=project_id,
    dataset_name=os.getenv("DATASET"),
    table_name=os.getenv("TABLE"),
    location=os.getenv("REGION"),
    embedding=embedding,
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    project=project_id,
    location="us-central1",
    vertexai=True,
)

prompt = PromptTemplate(
    input_variables=["question", "docs"],
    template="""You answer questions about Google Cloud certifications.
Use only the information in the documents below. If the answer is not there,
say that you could not find it in the documents.

Documents:
{docs}

Question: {question}
Answer:""",
)

def ai_helper(query, exam="Both"):
    sources = {
        "Associate Cloud Engineer":
            "https://services.google.com/fh/files/misc/associate_cloud_engineer_exam_guide_english.pdf",
        "Professional Cloud Security Engineer":
            "https://services.google.com/fh/files/misc/professional_cloud_security_engineer_exam_guide_english.pdf",
    }

    if exam == "Both":
        documents = vector_store.similarity_search(query, k=8)
    else:
        documents = vector_store.similarity_search(
            query,
            k=8,
            filter={"source": sources[exam]},
        )

    if not documents:
        return "I couldn't find relevant text in the selected guide.", []

    context = "\n\n".join(doc.page_content for doc in documents)

    chain = prompt | llm
    response = chain.invoke({"question": query, "docs": context})

    return response.content, documents