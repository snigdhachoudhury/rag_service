import time
import hashlib
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_document_id(url: str) -> str:
    """
    Generate a unique document ID based on URL
    """
    return hashlib.md5(url.encode()).hexdigest()

def measure_execution_time(func):
    """
    Decorator to measure function execution time
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"{func.__name__} executed in {execution_time:.2f} seconds")
        return result
    return wrapper

def validate_request_data(data: Dict[str, Any]) -> tuple[bool, str]:
    """
    Validate incoming request data
    """
    if not isinstance(data, dict):
        return False, "Request body must be a JSON object"
    
    if "documents" not in data:
        return False, "Missing 'documents' field in request"
    
    if "questions" not in data:
        return False, "Missing 'questions' field in request"
    
    if not isinstance(data["documents"], list):
        return False, "'documents' must be a list of URLs"
    
    if not isinstance(data["questions"], list):
        return False, "'questions' must be a list of strings"
    
    if len(data["documents"]) == 0:
        return False, "At least one document URL is required"
    
    if len(data["questions"]) == 0:
        return False, "At least one question is required"
    
    # Validate URLs
    for url in data["documents"]:
        if not isinstance(url, str) or not url.strip():
            return False, "All document URLs must be non-empty strings"
        if not (url.startswith("http://") or url.startswith("https://")):
            return False, f"Invalid URL format: {url}"
    
    # Validate questions
    for question in data["questions"]:
        if not isinstance(question, str) or not question.strip():
            return False, "All questions must be non-empty strings"
    
    return True, "Valid request"

def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split a list into chunks of specified size
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def sanitize_text(text: str) -> str:
    """
    Sanitize text for safe processing
    """
    if not isinstance(text, str):
        return ""
    
    # Remove potentially problematic characters
    text = text.replace('\x00', '')  # Null bytes
    text = text.replace('\ufffd', '')  # Replacement characters
    
    # Normalize whitespace
    text = ' '.join(text.split())
    
    return text.strip()

def format_error_response(error_message: str) -> Dict[str, List[str]]:
    """
    Format error message as a proper API response
    """
    return {
        "answers": [f"Error: {error_message}"]
    }

def log_performance_metrics(metrics: Dict[str, Any]):
    """
    Log performance metrics for monitoring
    """
    logger.info(f"Performance Metrics: {metrics}")

class PerformanceTracker:
    """
    Context manager for tracking performance metrics
    """
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.start_time = None
        self.metrics = {}
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        self.metrics['execution_time'] = end_time - self.start_time
        self.metrics['operation'] = self.operation_name
        if exc_type:
            self.metrics['error'] = str(exc_val)
        log_performance_metrics(self.metrics)
    
    def add_metric(self, key: str, value: Any):
        """Add a custom metric"""
        self.metrics[key] = value
