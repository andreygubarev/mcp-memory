import os
import hashlib
import chromadb

DATABASE = os.getenv("CHROMADB_DATABASE", "/data")

class Database:
    def __init__(self):
        if DATABASE:
            if not os.path.exists(DATABASE):
                raise ValueError(f"Database path {DATABASE} does not exist.")
            self.client = chromadb.PersistentClient(path=DATABASE)
        else:
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
            n_results=n_results,
        )
        if not results['documents']:
            return []

        return results
