from pydantic import BaseModel


class Sample(BaseModel):
    """Model for LLM completion samples."""

    id: str
    model: str
    prompt: str
    completion: str
    temperature: float | None = None


class Embedding(BaseModel):
    """Model for LLM embeddings."""

    model: str
    sample_id: str
    embedding: list[float]


class Similarity(BaseModel):
    """Model for pairwise similarity between samples."""

    model: str
    sample_id1: str
    sample_id2: str
    similarity: float
