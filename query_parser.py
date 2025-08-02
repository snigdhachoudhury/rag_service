import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Google Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

def parse_and_decompose_query(question: str) -> list[str]:
    """
    Step 2: LLM Parser
    Uses LLM to analyze complex queries and potentially break them down into sub-questions
    """
    try:
        # For simple questions, return as-is
        if len(question.split()) <= 10:
            return [question]
        
        # For complex questions, decompose using LLM
        decomposition_prompt = f"""
Analyze the following question and break it down into simpler, focused sub-questions if needed.
If it's already simple and focused, return just the original question.

Original question: "{question}"

Please return a list of focused sub-questions, one per line, that together would fully answer the original question.
If the question is already simple enough, just return the original question.

Sub-questions:
"""
        
        response = gemini_model.generate_content(
            decomposition_prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=300,
                temperature=0.1,
            )
        )
        
        sub_questions = response.text.strip().split('\n')
        # Clean up the sub-questions
        sub_questions = [q.strip().lstrip('- ').lstrip('1234567890. ') for q in sub_questions if q.strip()]
        
        return sub_questions if len(sub_questions) > 1 else [question]
        
    except Exception as e:
        print(f"Error in query decomposition: {e}")
        # Fallback to original question
        return [question]

def optimize_query_for_search(query: str) -> str:
    """
    Optimize a query for better embedding search by extracting key terms
    """
    try:
        optimization_prompt = f"""
Extract the key search terms and concepts from this question to make it better for semantic search.
Focus on the main topics, entities, and important concepts.

Original question: "{query}"

Optimized search query:
"""
        
        response = gemini_model.generate_content(
            optimization_prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=100,
                temperature=0.1,
            )
        )
        
        optimized = response.text.strip()
        return optimized if optimized else query
        
    except Exception as e:
        print(f"Error in query optimization: {e}")
        return query
