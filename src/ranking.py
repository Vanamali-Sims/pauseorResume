# src/ranking.py
import numpy as np
from numpy.linalg import norm

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Compute the cosine similarity between two vectors.
    """
    return float(np.dot(a, b) / (norm(a) * norm(b)))

def rank_resumes(job_embedding: np.ndarray, resume_embeddings: dict) -> list:
    """
    Rank resumes based on their cosine similarity to the job description.
    
    :param job_embedding: Embedding vector for the job description.
    :param resume_embeddings: Dictionary mapping resume IDs to embedding vectors.
    :return: List of tuples (resume_id, score) sorted in descending order.
    """
    scores = {}
    for resume_id, emb in resume_embeddings.items():
        scores[resume_id] = cosine_similarity(job_embedding, emb)
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked
