from sentence_transformers import SentenceTransformer

class EmbeddingGenerator:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # Load a small, fast, and good-quality embedding model
        self.model = SentenceTransformer(model_name)

    def generate(self, text: str):
        """
        Generate embeddings for a given text string.
        """
        return self.model.encode([text])[0]

    def generate_batch(self, texts):
        """
        Generate embeddings for a list of text chunks.
        """
        return self.model.encode(texts)
