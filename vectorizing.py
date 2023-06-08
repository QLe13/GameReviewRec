from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import DeepLake
from langchain.document_loaders import TextLoader
import os


os.environ["OPENAI_API_KEY"] = "urkey"
directory = 'Reviews'

embeddings = OpenAIEmbeddings()

# Loop through each file in the directory
for filename in os.listdir(directory):
    loader = TextLoader(os.path.join(directory, filename))
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_overlap=200)
    docs = text_splitter.split_documents(documents)
    db = DeepLake(dataset_path="./my_deeplake/"+filename.split('.')[0], embedding_function=embeddings)
    db.add_documents(docs)

