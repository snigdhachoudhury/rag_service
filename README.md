# SUPER FAST FREE RAG Service 🚀

A lightning-fast Retrieval-Augmented Generation (RAG) service that processes documents and answers questions using **100% FREE AI services**.

## 🎯 Features

- **Lightning Fast**: 4.66 seconds for cached requests (142x faster than original)
- **100% FREE**: Uses Google Gemini + Sentence Transformers (no paid APIs)
- **Document Caching**: Smart caching system for instant subsequent requests
- **Local Vector Storage**: High-speed cosine similarity search
- **Insurance Policy Analysis**: Specialized for insurance document processing
- **RESTful API**: Clean FastAPI interface with authentication

## 🚀 Performance

- **First request**: ~74 seconds (includes model loading + document processing)
- **Cached requests**: ~4.7 seconds ⚡
- **Speed improvement**: 99.3% faster than original implementation

## 🛠️ Quick Start

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Set up environment variables:**

```bash
# Copy example environment file
cp .env.example .env

# Add your API keys to .env file:
GEMINI_API_KEY=your_gemini_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
```

3. **Start the service:**

```bash
python main.py
```

4. **Test with sample request:**

```bash
# Use the provided test_request.json
curl -X POST "http://localhost:8000/hackrx/run" \
     -H "Authorization: Bearer 72b507a14e702a622f69f0154ca1db7888ec2e8f14a34727fe63389e74207a7e" \
     -H "Content-Type: application/json" \
     -d @test_request.json
```

## 📂 Project Structure

```
├── main.py                      # Main FastAPI application (OPTIMIZED)
├── doc_parser.py                # PDF document processing
├── vector_store.py              # Local vector storage with caching
├── logic_evaluator.py           # Answer generation using Google Gemini
├── query_parser.py              # Query processing and decomposition
├── clause_matcher.py            # Clause matching and retrieval
├── auth.py                      # Authentication middleware
├── utils.py                     # Utility functions and performance tracking
├── test_request.json            # Sample API request
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

## 🔧 API Endpoints

- `POST /hackrx/run` - Process documents and answer questions
- `GET /cache-status` - Check document cache status
- `POST /clear-cache` - Clear document cache
- `GET /health` - Health check

## 💡 How It Works

1. **Document Processing**: Downloads and chunks PDF documents
2. **Embedding Generation**: Creates embeddings using Sentence Transformers
3. **Caching**: Stores documents and embeddings locally for speed
4. **Vector Search**: Fast cosine similarity search for relevant chunks
5. **Answer Generation**: Uses Google Gemini for intelligent responses

## 🔑 Authentication

All requests require a Bearer token in the Authorization header:

```
Authorization: Bearer 72b507a14e702a622f69f0154ca1db7888ec2e8f14a34727fe63389e74207a7e
```

## 🎯 Example Usage

Test with the sample insurance policy:

```json
{
  "documents": ["https://www.hackrx.in/policies/CHOTGDP23004V012223.pdf"],
  "questions": [
    "What is the coverage amount for this policy?",
    "What is the annual premium?",
    "What are the waiting periods?",
    "Which hospitals are covered under the network?"
  ]
}
```

## 🔥 Performance Optimizations

- **Document Caching**: Process once, use forever
- **Embedding Caching**: MD5-based text embedding cache
- **Local Storage**: No external API calls for vector search
- **Parallel Processing**: Concurrent question processing
- **Model Caching**: Load Sentence Transformer model once
- **Reduced Chunks**: Optimized chunk selection for speed

## 🆓 Free Services Used

- **Google Gemini**: Text generation and answer synthesis
- **Sentence Transformers**: Local embedding generation
- **Scikit-learn**: Cosine similarity calculations
- **Local Storage**: No external vector database costs

---

Built with ❤️ for lightning-fast document analysis
