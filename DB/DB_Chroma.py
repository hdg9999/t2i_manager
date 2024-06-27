import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction, EmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader


class DB_chroma():
    client: chromadb.ClientAPI
    embedding_function: EmbeddingFunction
    image_loader: ImageLoader

    def __init__(self):
        self.client = chromadb.PersistentClient()
        self.embedding_function = OpenCLIPEmbeddingFunction()
        self.image_loader = ImageLoader()
        
    def create(self, collection_name:str):
        self.client.create_collection(collection_name, metadata={"hnsw:space": "cosine"}, data_loader=self.image_loader)

    def search(self, collection_name:str, query_texts:list[str]):
        collection = self.client.get_collection(name=collection_name, embedding_function=self.embedding_function)
        return collection.query(query_texts=query_texts)
    
    def add(self, collection_name:str, ids:list[str], image_files:list[str], file_info:list[dict]):
        self.client.get_collection(collection_name, embedding_function=self.embedding_function, data_loader=self.image_loader).add(ids=ids, uris=image_files, metadatas=file_info)

    def drop(self, collection_name:str):
        self.client.delete_collection(collection_name)

    

        