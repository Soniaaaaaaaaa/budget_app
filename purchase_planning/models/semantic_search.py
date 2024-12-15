from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams
import json

with open('api_file/config.json') as file:
    CONFIG = json.load(file)

class SemanticSearch:
    def __init__(self, group_id: int):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = QdrantClient(
            url=CONFIG['url'], 
            api_key=CONFIG['api_key'],
        )
        self.collection_name = f'group_id={group_id}'
        if not self.client.collection_exists(collection_name=self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=384, 
                    distance=Distance.COSINE
                ),
            )
        
    def find_similar(self, query: str):
        embedding = self.model.encode(query).tolist()
        res = self.client.search(
                collection_name=self.collection_name,
                query_vector = embedding, 
                limit=1
            )
        if len(res) == 0:
            return None
        res = res[0]
        if res.score < 0.60:
            return None
        return res.id
    
    def add_new_point(self, point_id: int, query: str):
        embedding = self.model.encode(query).tolist()
        point = PointStruct(
            id=point_id,
            payload={'item': query},
            vector=embedding,
        )
        self.client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )
