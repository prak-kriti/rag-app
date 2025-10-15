import os
import faiss
import numpy as np
import pickle

class VectorStore:
    def __init__(self, index_path="vector_store"):
        self.index_path = index_path
        self.index_file = os.path.join(index_path, "index.faiss")
        self.meta_file = os.path.join(index_path, "metadata.pkl")

        os.makedirs(index_path, exist_ok=True)

        # Load or create FAISS index
        if os.path.exists(self.index_file):
            self.index = faiss.read_index(self.index_file)
            with open(self.meta_file, "rb") as f:
                self.texts = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(384)  # 384 = embedding dim of MiniLM
            self.texts = []

    def add_embeddings(self, embeddings, texts):
        """Add new embeddings and their corresponding texts to the index."""
        embeddings = np.array(embeddings).astype("float32")
        self.index.add(embeddings)
        self.texts.extend(texts)

        # Save updated index and metadata
        faiss.write_index(self.index, self.index_file)
        with open(self.meta_file, "wb") as f:
            pickle.dump(self.texts, f)

    def query(self, embedding, top_k=3):
        """Retrieve top_k most similar text chunks."""
        if len(self.texts) == 0:
            return ["No data in the index. Please ingest first."]
        embedding = np.array([embedding]).astype("float32")
        distances, indices = self.index.search(embedding, top_k)
        results = [self.texts[i] for i in indices[0] if i < len(self.texts)]
        return results
