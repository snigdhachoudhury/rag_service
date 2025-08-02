"""
SUPER FAST Vector Store - Local storage with FREE embeddings
"""
import os
import time
import logging
import hashlib
import pickle
import json
from typing import List, Tuple, Dict
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global caches
model_cache = None
embeddings_cache = {}
documents_store = {}  # Local document storage

def get_model():
    """Get cached model instance"""
    global model_cache
    if model_cache is None:
        logger.info("Loading Sentence Transformer model (one-time operation)...")
        model_cache = SentenceTransformer('all-MiniLM-L6-v2')
        logger.info("✅ Model loaded and cached")
    return model_cache

def get_text_hash(text: str) -> str:
    """Generate hash for text to use as cache key"""
    return hashlib.md5(text.encode()).hexdigest()

def embed_text_super_fast(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings with aggressive caching
    """
    if not texts:
        return []
        
    model = get_model()
    
    # Check cache first
    embeddings = []
    texts_to_embed = []
    
    for text in texts:
        text_hash = get_text_hash(text)
        if text_hash in embeddings_cache:
            embeddings.append(embeddings_cache[text_hash])
        else:
            # Add to batch for processing
            texts_to_embed.append((text, text_hash))
            embeddings.append(None)  # Placeholder
    
    # Generate embeddings for non-cached texts
    if texts_to_embed:
        logger.info(f"Generating embeddings for {len(texts_to_embed)} new texts")
        batch_texts = [item[0] for item in texts_to_embed]
        new_embeddings = model.encode(batch_texts, batch_size=64, show_progress_bar=False)
        
        # Cache and fill results
        embed_idx = 0
        for i, text in enumerate(texts):
            if embeddings[i] is None:  # Not cached
                text_hash = texts_to_embed[embed_idx][1]
                embedding = new_embeddings[embed_idx].tolist()
                embeddings_cache[text_hash] = embedding
                embeddings[i] = embedding
                embed_idx += 1
    
    return embeddings

def store_embeddings_super_fast(chunks: List[str], document_id: str) -> bool:
    """
    Store document chunks in local storage with embeddings
    """
    try:
        logger.info(f"🚀 SUPER FAST storing {len(chunks)} chunks for document {document_id}")
        
        # Check if already stored
        if document_id in documents_store:
            logger.info(f"✅ Document {document_id} already in cache")
            return True
        
        # Generate embeddings
        embeddings = embed_text_super_fast(chunks)
        
        # Store locally
        documents_store[document_id] = {
            "chunks": chunks,
            "embeddings": embeddings,
            "timestamp": time.time()
        }
        
        logger.info(f"✅ SUPER FAST stored {len(chunks)} chunks locally")
        return True
        
    except Exception as e:
        logger.error(f"Error storing embeddings: {e}")
        return False

def search_similar_chunks_super_fast(query: str, top_k: int = 10) -> List[Tuple[str, float]]:
    """
    Search for similar chunks using local cosine similarity
    """
    try:
        if not documents_store:
            logger.warning("No documents stored locally")
            return []
        
        # Generate query embedding
        query_embedding = embed_text_super_fast([query])[0]
        query_vector = np.array(query_embedding).reshape(1, -1)
        
        # Search all stored documents
        all_chunks = []
        all_embeddings = []
        
        for doc_id, doc_data in documents_store.items():
            all_chunks.extend(doc_data["chunks"])
            all_embeddings.extend(doc_data["embeddings"])
        
        if not all_embeddings:
            return []
        
        # Compute similarities
        embeddings_matrix = np.array(all_embeddings)
        similarities = cosine_similarity(query_vector, embeddings_matrix)[0]
        
        # Get top_k results
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            chunk = all_chunks[idx]
            score = float(similarities[idx])
            results.append((chunk, score))
        
        logger.info(f"✅ Found {len(results)} similar chunks with LOCAL search")
        return results
        
    except Exception as e:
        logger.error(f"Error searching similar chunks: {e}")
        return []

def get_cache_stats():
    """Get cache statistics"""
    total_chunks = sum(len(doc["chunks"]) for doc in documents_store.values())
    return {
        "cached_embeddings": len(embeddings_cache),
        "stored_documents": len(documents_store),
        "total_chunks": total_chunks,
        "model_loaded": model_cache is not None
    }

def clear_all_cache():
    """Clear all caches"""
    global embeddings_cache, documents_store
    embeddings_cache = {}
    documents_store = {}
    return {"message": "All caches cleared"}

# Aliases for backward compatibility
store_embeddings = store_embeddings_super_fast
search_similar_chunks = search_similar_chunks_super_fast
embed_text = embed_text_super_fast
