import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import List, Tuple

load_dotenv()

# Configure Google Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

def rerank_chunks_with_llm(query: str, chunks: List[str], top_k: int = 5) -> List[str]:
    """
    Step 4: Clause Matching
    Re-rank retrieved chunks using LLM for better relevance scoring
    """
    if not chunks:
        return []
    
    try:
        # If we have fewer chunks than top_k, return all of them
        if len(chunks) <= top_k:
            return chunks
        
        # Create a prompt for the LLM to score relevance
        chunk_text = ""
        for i, chunk in enumerate(chunks):
            chunk_text += f"\n[Chunk {i+1}]: {chunk}\n"
        
        rerank_prompt = f"""
You are an expert document analyst. Given a user question and multiple text chunks from a document, 
rank the chunks by their relevance to answering the question.

Question: "{query}"

Text Chunks:
{chunk_text}

Please rank the chunks from most relevant (1) to least relevant ({len(chunks)}) for answering the question.
Only return the chunk numbers in order, separated by commas.
For example: 3, 1, 7, 2, 5

Ranking:
"""
        
        response = gemini_model.generate_content(
            rerank_prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=100,
                temperature=0.1,
            )
        )
        
        ranking_str = response.text.strip()
        
        # Parse the ranking
        try:
            rankings = [int(x.strip()) - 1 for x in ranking_str.split(',')]  # Convert to 0-based index
            # Validate rankings
            rankings = [r for r in rankings if 0 <= r < len(chunks)]
            
            # Return top_k chunks in the ranked order
            reranked_chunks = [chunks[i] for i in rankings[:top_k] if i < len(chunks)]
            
            # If we don't have enough from ranking, add remaining chunks
            if len(reranked_chunks) < top_k:
                used_indices = set(rankings[:top_k])
                for i, chunk in enumerate(chunks):
                    if i not in used_indices and len(reranked_chunks) < top_k:
                        reranked_chunks.append(chunk)
            
            return reranked_chunks
            
        except (ValueError, IndexError) as e:
            print(f"Error parsing rankings: {e}")
            # Fallback to original order
            return chunks[:top_k]
        
        response = gemini_model.generate_content(
            rerank_prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=100,
                temperature=0.1,
            )
        )
        
        ranking_str = response.text.strip()
        
        # Parse the ranking
        try:
            rankings = [int(x.strip()) - 1 for x in ranking_str.split(',')]  # Convert to 0-based index
            # Validate rankings
            rankings = [r for r in rankings if 0 <= r < len(chunks)]
            
            # Return top_k chunks in the ranked order
            reranked_chunks = [chunks[i] for i in rankings[:top_k] if i < len(chunks)]
            
            # If we don't have enough from ranking, add remaining chunks
            if len(reranked_chunks) < top_k:
                used_indices = set(rankings[:top_k])
                for i, chunk in enumerate(chunks):
                    if i not in used_indices and len(reranked_chunks) < top_k:
                        reranked_chunks.append(chunk)
            
            return reranked_chunks
            
        except (ValueError, IndexError) as e:
            print(f"Error parsing rankings: {e}")
            # Fallback to original order
            return chunks[:top_k]
            
    except Exception as e:
        print(f"Error in LLM reranking: {e}")
        # Fallback to original order
        return chunks[:top_k]

def filter_relevant_chunks(query: str, chunks: List[str], relevance_threshold: float = 0.7) -> List[str]:
    """
    Filter chunks based on relevance to the query using LLM
    """
    if not chunks:
        return []
    
    try:
        relevant_chunks = []
        
        for chunk in chunks:
            relevance_prompt = f"""
Rate the relevance of this text chunk to the given question on a scale of 0.0 to 1.0.
- 1.0 = Directly answers the question or contains the exact information needed
- 0.7-0.9 = Contains relevant information that helps answer the question
- 0.4-0.6 = Somewhat related but not directly helpful
- 0.0-0.3 = Not relevant to the question

Question: "{query}"

Text Chunk: "{chunk}"

Relevance Score (0.0 to 1.0):
"""
            
            response = gemini_model.generate_content(
                relevance_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=10,
                    temperature=0.1,
                )
            )
            
            try:
                score = float(response.text.strip())
                if score >= relevance_threshold:
                    relevant_chunks.append(chunk)
            except ValueError:
                # If we can't parse the score, include the chunk to be safe
                relevant_chunks.append(chunk)
        
        return relevant_chunks
        
    except Exception as e:
        print(f"Error in relevance filtering: {e}")
        # Fallback to returning all chunks
        return chunks

def semantic_chunk_matching(query: str, chunks: List[str], max_chunks: int = 5) -> List[str]:
    """
    Main function that combines reranking and filtering for optimal chunk selection
    """
    if not chunks:
        return []
    
    # First, rerank the chunks
    reranked_chunks = rerank_chunks_with_llm(query, chunks, top_k=min(10, len(chunks)))
    
    # Then filter for relevance
    relevant_chunks = filter_relevant_chunks(query, reranked_chunks, relevance_threshold=0.6)
    
    # Return up to max_chunks
    return relevant_chunks[:max_chunks]
        print(f"Error in LLM reranking: {e}")
        # Fallback to original order
        return chunks[:top_k]

def filter_relevant_chunks(query: str, chunks: List[str], relevance_threshold: float = 0.7) -> List[str]:
    """
    Filter chunks based on relevance to the query using LLM
    """
    if not chunks:
        return []
    
    try:
        relevant_chunks = []
        
        for chunk in chunks:
            relevance_prompt = f"""
Rate the relevance of this text chunk to the given question on a scale of 0.0 to 1.0.
- 1.0 = Directly answers the question or contains the exact information needed
- 0.7-0.9 = Contains relevant information that helps answer the question
- 0.4-0.6 = Somewhat related but not directly helpful
- 0.0-0.3 = Not relevant to the question

Question: "{query}"

Text Chunk: "{chunk}"

Relevance Score (0.0 to 1.0):
"""
            
            response = gemini_model.generate_content(
                relevance_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=10,
                    temperature=0.1,
                )
            )
            
            try:
                score = float(response.text.strip())
                if score >= relevance_threshold:
                    relevant_chunks.append(chunk)
            except ValueError:
                # If we can't parse the score, include the chunk to be safe
                relevant_chunks.append(chunk)
        
        return relevant_chunks
        
    except Exception as e:
        print(f"Error in relevance filtering: {e}")
        # Fallback to returning all chunks
        return chunks

def semantic_chunk_matching(query: str, chunks: List[str], max_chunks: int = 5) -> List[str]:
    """
    Main function that combines reranking and filtering for optimal chunk selection
    """
    if not chunks:
        return []
    
    # First, rerank the chunks
    reranked_chunks = rerank_chunks_with_llm(query, chunks, top_k=min(10, len(chunks)))
    
    # Then filter for relevance
    relevant_chunks = filter_relevant_chunks(query, reranked_chunks, relevance_threshold=0.6)
    
    # Return up to max_chunks
    return relevant_chunks[:max_chunks]

# Legacy function to maintain compatibility
def filter_relevant_chunks_legacy(question, chunks):
    """Legacy function - kept for backward compatibility"""
    prompt = f"""Given the question: "{question}"\nAnd the following clauses:\n\n"""
    for i, chunk in enumerate(chunks):
        prompt += f"Clause {i+1}: {chunk}\n\n"
    prompt += "Return only the clauses that directly help answer the question."

    response = gemini_model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=500,
            temperature=0,
        )
    )
    return response.text
