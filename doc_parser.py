import requests
import pdfplumber
import os
import hashlib
from nltk.tokenize import sent_tokenize
from typing import List, Tuple
import nltk

# Download NLTK data if not present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def download_pdf(url: str, download_dir: str = "temp_docs") -> str:
    """
    Step 1: Input Documents (Part 1)
    Download PDF from URL and save locally
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(download_dir, exist_ok=True)
        
        # Generate filename based on URL hash to avoid conflicts
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        filename = f"doc_{url_hash}.pdf"
        filepath = os.path.join(download_dir, filename)
        
        # Download the file
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        
        with open(filepath, "wb") as f:
            f.write(response.content)
        
        return filepath
        
    except Exception as e:
        print(f"Error downloading PDF from {url}: {e}")
        raise

def extract_and_chunk_text(pdf_path: str, chunk_size: int = 800, overlap: int = 100) -> List[str]:
    """
    Step 1: Input Documents (Part 2)
    Extract text from PDF and split into meaningful chunks with overlap
    """
    try:
        chunks = []
        
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            
            # Extract text from all pages
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"
            
            if not full_text.strip():
                return ["No text could be extracted from this document."]
            
            # Clean the text
            full_text = clean_text(full_text)
            
            # Split into sentences first
            sentences = sent_tokenize(full_text)
            
            current_chunk = []
            current_length = 0
            
            for sentence in sentences:
                sentence_length = len(sentence)
                
                # If adding this sentence would exceed chunk_size, save current chunk
                if current_length + sentence_length > chunk_size and current_chunk:
                    chunk_text = " ".join(current_chunk)
                    chunks.append(chunk_text)
                    
                    # Create overlap by keeping last few sentences
                    overlap_sentences = []
                    overlap_length = 0
                    for sent in reversed(current_chunk):
                        if overlap_length + len(sent) <= overlap:
                            overlap_sentences.insert(0, sent)
                            overlap_length += len(sent)
                        else:
                            break
                    
                    current_chunk = overlap_sentences
                    current_length = overlap_length
                
                current_chunk.append(sentence)
                current_length += sentence_length
            
            # Add the last chunk if it exists
            if current_chunk:
                chunk_text = " ".join(current_chunk)
                chunks.append(chunk_text)
        
        # Filter out very short chunks
        chunks = [chunk for chunk in chunks if len(chunk.strip()) > 50]
        
        return chunks if chunks else ["No meaningful text could be extracted from this document."]
        
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return [f"Error processing document: {str(e)}"]

def clean_text(text: str) -> str:
    """
    Clean extracted text by removing excessive whitespace and formatting issues
    """
    # Replace multiple whitespace with single space
    text = ' '.join(text.split())
    
    # Remove common PDF artifacts
    text = text.replace('\x00', '')  # Null characters
    text = text.replace('\ufffd', '')  # Replacement characters
    
    # Fix common spacing issues around punctuation
    text = text.replace(' .', '.')
    text = text.replace(' ,', ',')
    text = text.replace(' ;', ';')
    text = text.replace(' :', ':')
    
    return text.strip()

def extract_document_metadata(pdf_path: str) -> dict:
    """
    Extract metadata from PDF document
    """
    metadata = {
        "filename": os.path.basename(pdf_path),
        "file_size": 0,
        "page_count": 0,
        "title": "",
        "author": "",
        "creation_date": None
    }
    
    try:
        metadata["file_size"] = os.path.getsize(pdf_path)
        
        with pdfplumber.open(pdf_path) as pdf:
            metadata["page_count"] = len(pdf.pages)
            
            # Extract PDF metadata
            if pdf.metadata:
                metadata["title"] = pdf.metadata.get("Title", "")
                metadata["author"] = pdf.metadata.get("Author", "")
                metadata["creation_date"] = pdf.metadata.get("CreationDate")
                
    except Exception as e:
        print(f"Error extracting metadata from {pdf_path}: {e}")
    
    return metadata

def process_document_url(url: str) -> Tuple[List[str], dict]:
    """
    Complete document processing pipeline: download, extract, chunk, and get metadata
    """
    try:
        # Download the document
        pdf_path = download_pdf(url)
        
        # Extract metadata
        metadata = extract_document_metadata(pdf_path)
        
        # Extract and chunk text
        chunks = extract_and_chunk_text(pdf_path)
        
        # Clean up temporary file
        try:
            os.remove(pdf_path)
        except:
            pass  # Ignore cleanup errors
        
        return chunks, metadata
        
    except Exception as e:
        error_msg = f"Failed to process document from {url}: {str(e)}"
        return [error_msg], {"error": error_msg}
