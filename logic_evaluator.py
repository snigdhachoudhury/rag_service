import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

# Configure Google Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

def generate_answer_with_citations(question: str, relevant_chunks: List[str]) -> str:
    """
    Step 5: Logic Evaluation
    Generate a comprehensive answer based on relevant context chunks with proper citations
    """
    if not relevant_chunks:
        return "I cannot find any relevant information in the provided document to answer this question."
    
    # Prepare the context with numbered chunks for citation
    context_text = ""
    for i, chunk in enumerate(relevant_chunks, 1):
        context_text += f"[Source {i}]: {chunk}\n\n"
    
    prompt = f"""
You are an expert document analyst. Based on the provided context from a document, answer the user's question accurately and thoroughly.

IMPORTANT INSTRUCTIONS:
1. Base your answer ONLY on the information provided in the context below
2. If the context doesn't contain enough information to answer the question, clearly state this
3. Always cite your sources using [Source X] notation when referencing specific information
4. Be precise and avoid speculation or information not present in the context
5. If there are conditions, limitations, or requirements mentioned, include them in your answer
6. Structure your answer clearly and logically

Question: "{question}"

Context from Document:
{context_text}

Answer:
"""

    try:
        response = gemini_model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=800,
                temperature=0.1,
            )
        )
        
        return response.text.strip()
        
    except Exception as e:
        print(f"Error generating answer: {e}")
        return f"I apologize, but I encountered an error while processing your question: {str(e)}"

def synthesize_multiple_sources(question: str, sub_answers: List[str]) -> str:
    """
    Combine answers from multiple sub-questions into a coherent response
    """
    if not sub_answers:
        return "No relevant information found to answer the question."
    
    if len(sub_answers) == 1:
        return sub_answers[0]
    
    synthesis_prompt = f"""
You have answers to multiple related sub-questions for the main question: "{question}"

Sub-answers:
"""
    for i, answer in enumerate(sub_answers, 1):
        synthesis_prompt += f"\nAnswer {i}: {answer}\n"
    
    synthesis_prompt += """
Please synthesize these answers into a single, coherent, and comprehensive response to the main question.
Remove any redundancy and ensure the answer flows logically. Maintain all citations from the sub-answers.

Synthesized Answer:
"""

    try:
        response = gemini_model.generate_content(
            synthesis_prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=1000,
                temperature=0.1,
            )
        )
        
        return response.text.strip()
        
    except Exception as e:
        print(f"Error synthesizing answers: {e}")
        # Fallback to combining answers
        return "\n\n".join(sub_answers)

# Legacy function for backward compatibility
def generate_answer(question, context):
    """Legacy function - kept for backward compatibility"""
    prompt = f"""You are a legal assistant. Given the question:\n"{question}"\n\nAnd the relevant policy context:\n{context}\n\nAnswer the question precisely. If you can't find the answer, say "Not mentioned in document." Cite supporting sentences."""
    
    response = gemini_model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=500,
            temperature=0.3,
        )
    )
    return response.text
