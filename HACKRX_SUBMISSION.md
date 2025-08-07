# HackRX Submission Information

## Webhook URL

**Format**: `https://your-deployed-url.com/hackrx/run`
**Local**: `http://localhost:8000/hackrx/run` (needs public deployment)

## API Specification

- **Method**: POST
- **Content-Type**: application/json
- **Authorization**: Bearer 72b507a14e702a622f69f0154ca1db7888ec2e8f14a34727fe63389e74207a7e

## Sample Request Format

```json
{
  "documents": ["https://hackrx.blob.core.windows.net/assets/policy.pdf"],
  "questions": [
    "What is the grace period for premium payment?",
    "What is the waiting period for pre-existing diseases?"
  ]
}
```

## Expected Response Format

```json
{
  "answers": [
    "Detailed answer 1 with source citations...",
    "Detailed answer 2 with source citations..."
  ]
}
```

## Performance Metrics

- **Response Time**: 9-38 seconds (depending on document size)
- **Document Processing**: Supports PDF documents up to 276 chunks
- **Caching**: Subsequent requests are 50%+ faster
- **Error Handling**: Graceful handling of inaccessible documents

## Technology Stack

- **AI Models**: 100% FREE (Google Gemini + Sentence Transformers)
- **Framework**: FastAPI with async processing
- **Vector Storage**: Local cosine similarity search
- **Caching**: Intelligent document and embedding caching

## Tested Documents

✅ BAJAJ Insurance Policy (276 chunks, 37.98s)
✅ Arogya Sanjeevani Policy (110 chunks, 19.66s)
✅ Multiple document formats and error scenarios

## Repository

GitHub: https://github.com/snigdhachoudhury/rag_service
Branch: main
Ready for deployment to any cloud platform
