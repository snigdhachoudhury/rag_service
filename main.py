"""
SUPER FAST Version of main.py - Ultra-optimized FREE RAG service
"""
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import asyncio
import gc
import logging
from datetime import datetime

# Import SUPER FAST modules
import doc_parser
from vector_store import store_embeddings, search_similar_chunks, get_cache_stats, clear_all_cache
from logic_evaluator import generate_answer_with_citations
from auth import verify_token
from utils import generate_document_id, PerformanceTracker, format_error_response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SUPER FAST FREE RAG Service API", version="3.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache for processed documents
processed_documents = {}

class RunRequest(BaseModel):
    documents: List[str]
    questions: List[str]

@app.get("/")
async def root():
    return {
        "message": "SUPER FAST FREE RAG Service API is running", 
        "status": "healthy", 
        "powered_by": "Google Gemini + Sentence Transformers + Local Storage",
        "speed": "Ultra Optimized"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "super-fast-free-rag-service", 
        "ai_providers": ["Google Gemini", "Sentence Transformers"],
        "storage": "Local Cache"
    }

@app.post("/hackrx/run")
async def run_pipeline(request: Request, body: RunRequest):
    """
    SUPER FAST FREE RAG pipeline - ultra-optimized for speed
    """
    with PerformanceTracker("super_fast_pipeline") as tracker:
        try:
            # Verify authentication
            verify_token(request)
            
            # Validate input
            if not body.documents or not body.questions:
                raise HTTPException(status_code=400, detail="Both documents and questions are required")
            
            # Track request
            tracker.add_metric("documents_count", len(body.documents))
            tracker.add_metric("questions_count", len(body.questions))
            
            # Step 1: Process documents (with caching)
            for doc_url in body.documents:
                doc_id = generate_document_id(doc_url)
                
                if doc_id not in processed_documents:
                    logger.info(f"🚀 Processing NEW document: {doc_url}")
                    try:
                        chunks, metadata = doc_parser.process_document_url(doc_url)
                        
                        # Store using SUPER FAST local storage
                        success = store_embeddings(chunks, doc_id)
                        if success:
                            processed_documents[doc_id] = {
                                "url": doc_url,
                                "chunks": len(chunks),
                                "processed_at": datetime.now().isoformat()
                            }
                            logger.info(f"✅ Cached document {doc_id} with {len(chunks)} chunks")
                        
                    except Exception as e:
                        logger.error(f"Error processing document {doc_url}: {e}")
                        continue
                else:
                    logger.info(f"⚡ Using CACHED document: {doc_id}")
            
            # Process questions in parallel (for speed)
            import concurrent.futures
            
            answers = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                future_to_question = {
                    executor.submit(process_question_super_fast, question, tracker): question 
                    for question in body.questions
                }
                
                for future in concurrent.futures.as_completed(future_to_question):
                    question = future_to_question[future]
                    try:
                        answer = future.result()
                        answers.append(answer)
                    except Exception as e:
                        logger.error(f"Error processing question '{question}': {e}")
                        answers.append(f"Error processing question: {str(e)}")
            
            # Force garbage collection to free memory
            gc.collect()
            return {"answers": answers}
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in SUPER FAST pipeline: {e}")
            return format_error_response(f"Internal server error: {str(e)}")

def process_question_super_fast(question: str, tracker: PerformanceTracker) -> str:
    """
    Process a single question SUPER FAST - minimal operations
    """
    try:
        # Direct vector search with fewer chunks
        similar_chunks = search_similar_chunks(question, top_k=3)  # Reduced from 5 to 3
        
        if not similar_chunks:
            return "I cannot find relevant information in the provided documents to answer this question."
        
        tracker.add_metric("chunks_used", len(similar_chunks))
        
        # Direct answer generation
        answer = generate_answer_with_citations(question, similar_chunks)
        return answer
        
    except Exception as e:
        logger.error(f"Error in process_question_super_fast: {e}")
        return f"I apologize, but I encountered an error: {str(e)}"

@app.get("/cache-status")
async def cache_status():
    """Check cached documents and embeddings"""
    cache_stats = get_cache_stats()
    return {
        "processed_documents": len(processed_documents),
        "documents": processed_documents,
        "cache_stats": cache_stats,
        "performance": "Subsequent requests will be lightning fast"
    }

@app.post("/clear-cache")
async def clear_cache():
    """Clear all caches for testing"""
    global processed_documents
    processed_documents = {}
    clear_result = clear_all_cache()
    return {
        "message": "All caches cleared", 
        "processed_documents": 0,
        "cache_result": clear_result
    }

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
