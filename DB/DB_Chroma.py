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
    #RGB 혹은 JPG 형식 이미지로 변환하지 않으면 ValueError: Unable to infer channel dimension format 발생하기 때문에 convert("RGB")만 추가한 코드로 오버라이드해서 사용
    @override
    def _load_image(self, uri: Optional[URI]) -> Optional[Image]:        
        return np.array(self._PILImage.open(uri).convert("RGB")) if uri is not None else None


class KoCLIPEmbeddingFunction(EmbeddingFunction[Union[Documents, Images]]):
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

        print('\t\t##input:',input)

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
        ## KoCLIP대신 OpenCLIP 사용하려면 KoCLIP 관련 클래스 대신 주석처리된 부분 해제하여 사용. 이 경우 프로그램이 약간 더 가벼워지는것 같지만 한글 검색이 안됨.
        self.client = chromadb.PersistentClient()
        # self.embedding_function = OpenCLIPEmbeddingFunction()
        self.embedding_function = KoCLIPEmbeddingFunction()
        # self.image_loader = ImageLoader()
        self.image_loader = ImageLoaderForKoCLIP()
        
    #client 함수
    def create(self, collection_name:str):
        self.client.create_collection(collection_name, metadata={"hnsw:space": "cosine"}, data_loader=self.image_loader)

    def get_or_create(self, collection_name:str):
        self.client.get_or_create_collection(collection_name, metadata={"hnsw:space": "cosine"}, data_loader=self.image_loader)
        
    def drop(self, collection_name:str):
        self.client.delete_collection(collection_name)
    
    def get_img_collection(self, collection_name):
        return self.client.get_collection(name=collection_name, embedding_function=self.embedding_function, data_loader=self.image_loader)

    #collection 함수
    def get(self, collection_name:str, ids:str):
        collection = self.get_img_collection(collection_name)
        return collection.get(ids)

    def search(self, collection_name:str, query_texts:list[str], where:list[dict]|None, top_k:10):
        collection = self.get_img_collection(collection_name)
        where_expression = None
        if where:
            #검색할 태그가 한개밖에 없는 경우 '$and' operator 사용하면 안됨.
            if len(where) !=1:
                where_expression = {'$and':where}
            else:
                where_expression = where[0]
        print(where_expression)
        return collection.query(query_texts=query_texts, where=where_expression, n_results=top_k)
    
    def add(self, collection_name:str, ids:str|list[str], image_files:str|list[str], file_info:dict|list[dict]):
        self.get_img_collection(collection_name).add(ids=ids, uris=image_files, metadatas=file_info)

    def update(self, collection_name:str, id:str, file_path:str, metadata:dict):
        self.get_img_collection(collection_name).update(ids=id, uris=file_path, metadatas=metadata)

    def upsert(self, collection_name:str, ids:str|list[str], image_files:str|list[str], file_info:dict|list[dict]):
        print('DB_upsert:', collection_name, ' / ',ids,' / ',image_files,' / ',file_info)
        self.get_img_collection(collection_name).upsert(ids=ids, uris=image_files, metadatas=file_info)

    def delete(self, collection_name:str, ids:str):
        self.get_img_collection(collection_name).delete(ids=ids)    
    


DB_CLIENT = DB_chroma()

    

        