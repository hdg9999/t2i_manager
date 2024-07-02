import chromadb
import pprint
import numpy as np
from overrides import override
import torch
from typing import Optional, Union
from chromadb import Documents, EmbeddingFunction, Embeddings
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction, EmbeddingFunction
from chromadb.api.types import Images, Image, is_document, is_image, URI
from chromadb.utils.data_loaders import ImageLoader

from transformers import AutoProcessor, AutoModel, VisionTextDualEncoderProcessor, VisionTextDualEncoderModel


class ImageLoaderForKoCLIP(ImageLoader):
    #RGB 혹은 JPG 타입 이미지로 변환하지 않으면 ValueError: Unable to infer channel dimension format 발생하기 때문에 convert("RGB")만 추가한 코드로 오버라이드해서 사용
    @override
    def _load_image(self, uri: Optional[URI]) -> Optional[Image]:        
        return np.array(self._PILImage.open(uri).convert("RGB")) if uri is not None else None


class KoCLIPEmbeddingFunction(EmbeddingFunction):
    #한국어 지원하는 KoCLIP 모델 사용을 위한 Custom EmbeddingFunction 작성
    def __call__(self, input: Union[Documents, Images]) -> Embeddings:
        embeddings: Embeddings = []
        local_koclip_path = '.koclip'
        hf_koclip_repo_name = 'koclip/koclip-base-pt'
        try:
            processor= AutoProcessor.from_pretrained(local_koclip_path)
            model= AutoModel.from_pretrained(local_koclip_path)
        except:
            print('\t## koclip 모델이 없습니다. huggingface에서 다운로드받습니다.')
            processor:VisionTextDualEncoderProcessor = AutoProcessor.from_pretrained(hf_koclip_repo_name)
            model:VisionTextDualEncoderModel = AutoModel.from_pretrained(hf_koclip_repo_name)
            processor.save_pretrained(local_koclip_path)
            model.save_pretrained(local_koclip_path)
        finally:
            print('\t# koclip 로드 성공')

        with torch.no_grad():
            for item in input:        
                if is_image(item):
                    pre_processed = processor(images=item, return_tensors="pt", padding=True)
                    #squeeze() 해야 validate_embeddings 부분에서 오류 안남
                    embedding = model.get_image_features(**pre_processed).squeeze().tolist()
                    embeddings.append(embedding)
                elif is_document(item):
                    pre_processed = processor(text=item, return_tensors="pt", padding=True)
                    #squeeze() 해야 validate_embeddings 부분에서 오류 안남
                    embedding = model.get_text_features(**pre_processed).squeeze().tolist()
                    embeddings.append(embedding)                

        # pprint.pp(embeddings)
        return embeddings

class DB_chroma():
    client: chromadb.ClientAPI
    embedding_function: EmbeddingFunction
    image_loader: ImageLoader

    def __init__(self):
        self.client = chromadb.PersistentClient()
        # self.embedding_function = OpenCLIPEmbeddingFunction()
        self.embedding_function = KoCLIPEmbeddingFunction()
        # self.image_loader = ImageLoader()
        self.image_loader = ImageLoaderForKoCLIP()
        
    def create(self, collection_name:str):
        self.client.create_collection(collection_name, metadata={"hnsw:space": "cosine"}, data_loader=self.image_loader)
        # self.client.create_collection(collection_name, data_loader=self.image_loader)

    def get(self, collection_name:str, ids:str):
        collection = self.client.get_collection(name=collection_name, embedding_function=self.embedding_function)
        return collection.get(ids)

    def search(self, collection_name:str, query_texts:list[str]):
        collection = self.client.get_collection(name=collection_name, embedding_function=self.embedding_function)
        return collection.query(query_texts=query_texts)
    
    def add(self, collection_name:str, ids:str|list[str], image_files:str|list[str], file_info:dict|list[dict]):
        self.client.get_collection(collection_name, embedding_function=self.embedding_function, data_loader=self.image_loader).add(ids=ids, uris=image_files, metadatas=file_info)

    def update(self, collection_name:str, id:str, file_path:str, metadata:dict):
        self.client.get_collection(collection_name, embedding_function=self.embedding_function, data_loader=self.image_loader).update(ids=id, uris=file_path, metadatas=metadata)

    def drop(self, collection_name:str):
        self.client.delete_collection(collection_name)
    


DB_CLIENT = DB_chroma()

    

        