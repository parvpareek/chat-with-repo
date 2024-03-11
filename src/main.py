import dotenv 
import os
from llama_index.readers.github import GithubRepositoryReader, GithubClient
from llama_index.core import (VectorStoreIndex, StorageContext, PromptTemplate, load_index_from_storage, Settings)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.openai import OpenAIEmbedding

def load_environ_vars():
    dotenv.load_dotenv()
    github_token = os.environ['GITHUB_TOKEN']
    # open_api = os.environ['OPEN_API_KEY']
    if github_token is None:
        print("Add the GITHUB_TOKEN environment variable in the .env file")
        exit()
    """if open_api is None:
        print("Add the OPEN_API_KEY environment variable. Read instrucitons in the readme")
        exit()"""
    return github_token

def load_data(github_token: str, owner: str, repo: str):
    github_client = GithubClient(github_token)
    
    loader = GithubRepositoryReader(
        github_client,
        owner=owner,
        repo=repo,
        filter_file_extensions=(
                [".py", ".ipynb", ".js", ".ts", ".md"],
                GithubRepositoryReader.FilterType.INCLUDE,
            ),
            verbose=False,
            concurrent_requests=5,
        )
    docs = loader.load_data(branch="main")
    return docs

def load_embedding_model():
    embedding_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5") 
    print("embedding model loaded")
    return embedding_model
    
    
def main():
    github_token = load_environ_vars()
    PERSIST_DIR = "./basic/storage"
    
    choice = input("Enter 1 to use OPEN API enter 0 to use loally setup llama2 model using Ollama:")
    if not os.path.exists(PERSIST_DIR):
        owner = input("Enter the username of the owner of the repo: ")
        repo = input("Enter the name of the repo: ")
        documents = load_data(github_token, owner, repo)
        try:
            if choice == '1':
                print("Open API is being used")
                embedding_model = OpenAIEmbedding()
                index = VectorStoreIndex.from_documents(documents)
            else:
                print("Ollama is being used")
                embedding_model = load_embedding_model()
                Settings.embed_model = embedding_model
                
                index = VectorStoreIndex.from_documents(
                    documents,
                    embed_model=embedding_model
                    )
        except Exception as  e:
            print(e)
            exit()
        print("Documents Indexed")


    else:
        # load the existing index
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)
        print("Already indexed data loaded")
        
    llama = Ollama(model="llama2", request_timeout=200.0)
    Settings.llm = llama
    query_engine = index.as_query_engine(llm=llama)
    qa_prompt_tmpl_str = (
            "Context information is below.\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "Given the context information above I want you to think step by step to answer the query in a crisp manner, incase case you don't know the answer say 'I don't know!'.\n"
            "Query: {query_str}\n"
            "Answer: "
            )

    qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)
    query_engine.update_prompts({"response_synthesizer:text_qa_template": qa_prompt_tmpl})
    print("Press ctr + c to exit")
    while True:
        query = input("Enter your query: ")
        response = query_engine.query(query)
        print(response)

    
if __name__ == "__main__":
    main()
