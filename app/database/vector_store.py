from fastembed import TextEmbedding
from qdrant_client import QdrantClient, models
import hashlib

client = QdrantClient(url="http://localhost:6333")

collections = client.get_collections().collections
if not any(c.name == "books" for c in collections):
    client.create_collection(
        collection_name="books",
        vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
    )

class VectorStore:
    def __init__(self):
        self.client = client
        self.embedder = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")


    def add_documents(self, book_title, chunks):
        texts = [chunk["text"] for chunk in chunks]
        embeddings = list(self.embedder.embed(texts))
        self.client.delete(
            collection_name="books",
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="book_title",
                            match=models.MatchValue(value=book_title),
                        )
                    ]
                )
            ),
        )
        self.client.upsert(
            collection_name="books",
            points=[
                models.PointStruct(
                    id=hashlib.md5(chunk["text"].encode()).hexdigest(),
                    vector=embedding,
                    payload={
                        "book_title": book_title,
                        "chunk_index": i,
                        "page": chunk["page"],
                        "text": chunk["text"]
                    }
                )
                for i, (embedding, chunk) in enumerate(zip(embeddings, chunks))
            ]
        )

    def query(self, book_title, query_text):
        query_vector = list(self.embedder.embed([query_text]))[0]
        result = self.client.query_points(
          collection_name="books",
          query=query_vector,
          query_filter=models.Filter(
            must=[
              models.FieldCondition(
                key="book_title",
                match=models.MatchValue(value=book_title),
              )
            ]
          ),
          search_params=models.SearchParams(hnsw_ef=128, exact=False),
          limit=10
        )
        return result.points

store = VectorStore()
