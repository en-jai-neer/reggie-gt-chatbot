from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import shutil

class GT_RAG():
    def __init__(self, cache_dir):
        model = HuggingFaceBgeEmbeddings(
            model_name = "all-MiniLM-L6-v2",
            cache_folder = "model_cache",
            encode_kwargs = {"normalize_embeddings" : True},
            model_kwargs={"device": "cpu"}
        )

        self.rag = Chroma(persist_directory=cache_dir, embedding_function=model)
    
    def query(self, q, k=10):
        related = self.rag.similarity_search_with_score(query=q, k=k)
        related = sorted(related, key = lambda x : x[1])
        related = [r[0].page_content for r in related]
        return ' '.join(related)

def calculate_vector_embeddings(input_dir, cache_dir):
    if os.path.isdir(cache_dir):
        shutil.rmtree(cache_dir)
        os.mkdir(cache_dir)

    model = HuggingFaceBgeEmbeddings(
        model_name = "all-MiniLM-L6-v2",
        cache_folder = "model_cache",
        encode_kwargs = {"normalize_embeddings" : True},
        model_kwargs={"device": "cpu"}
    )

    print("Emedding Data...")
    chroma_documents = []
    for src in os.listdir(input_dir):
        # load your pdf doc
        loader = PyPDFLoader(os.path.join(input_dir, src))
        pages = loader.load()

        # split the doc into smaller chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=150)
        chunks = text_splitter.split_documents(pages)

        chroma_documents += chunks
    print("Done!")

    print("Calculating embeddings and building database...")
    chroma_db = Chroma.from_documents(documents=chroma_documents, embedding=model, persist_directory=cache_dir)
    chroma_db.persist()
    print("Done!")

if __name__ == '__main__':
    # os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    calculate_vector_embeddings('RAG_data', 'RAG_cache')
    rag = GT_RAG('RAG_cache')
    res = rag.query("I want help with registering for a CS class")
    print(res)