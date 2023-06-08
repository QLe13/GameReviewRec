from langchain.vectorstores import DeepLake
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import os

os.environ["OPENAI_API_KEY"] = "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"
embeddings = OpenAIEmbeddings()

gameCode = input("Enter the game code: ")

db = DeepLake(dataset_path="./my_deeplake/"+gameCode, embedding_function=embeddings, read_only=True)
qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="map_reduce", retriever=db.as_retriever())

while True:
    query = input("Enter your query: ")
    if query == "exit":
        break
    else:
        print(qa.run(query))