import hashlib
import chromadb

class Database:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection("memory")

    def memorize(self, text: str):
        id = hashlib.sha256(text.encode()).hexdigest()
        self.collection.upsert(
            documents=[text],
            ids=[id]
        )

    def recall(self, query: str, n_results: int = 1):
        results = self.collection.query(
            query_texts=[query],
            n_results=1
        )
        if not results['documents']:
            return []

        return results['documents']
