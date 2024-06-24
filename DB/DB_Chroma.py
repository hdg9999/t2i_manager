import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction, EmbeddingFunction


class DB_chroma():
    client: chromadb.ClientAPI
    embedding_function: EmbeddingFunction

    def __init__(self):
        self.client = chromadb.PersistentClient()
        self.embedding_function = OpenCLIPEmbeddingFunction()

    def search(self, collection_name:str, query_texts:list[str]):
        collection = self.client.get_collection(name=collection_name, embedding_function=self.embedding_function)
        return collection.query(query_texts=query_texts)
    
    def create(self, collection_name:str, metadata:dict):
        self.client.create_collection(collection_name)

    def add(self, collection_name:str, images, file_info):
        self.client.get_collection(collection_name).add(images=[images], metadatas=[file_info])

        