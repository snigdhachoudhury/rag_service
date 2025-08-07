# Final submission test with alternative PDF
import requests
import json
import time

print("🚀 FINAL SUBMISSION TEST - SUPER FAST RAG SERVICE")
print("="*60)

# Test 1: Health Check
print("\n1. Testing Health Endpoint...")
health_response = requests.get("http://localhost:8000/health")
print(f"   Status: {health_response.status_code}")
print(f"   Response: {health_response.json()}")

# Test 2: Cache Status
print("\n2. Testing Cache Status...")
headers = {
    "Authorization": "Bearer 72b507a14e702a622f69f0154ca1db7888ec2e8f14a34727fe63389e74207a7e",
    "Content-Type": "application/json"
}
cache_response = requests.get("http://localhost:8000/cache-status", headers=headers)
print(f"   Status: {cache_response.status_code}")
print(f"   Cached Documents: {cache_response.json().get('cached_documents', 0)}")

# Test 3: Main RAG Pipeline with Insurance PDF
print("\n3. Testing Main RAG Pipeline...")
url = "http://localhost:8000/hackrx/run"
data = {
    "documents": ["https://www.hackrx.in/policies/CHOTGDP23004V012223.pdf"],
    "questions": [
        "What is the coverage amount for this policy?",
        "Does this policy cover knee surgery, and what are the conditions?"
    ]
}

print("   Processing insurance policy PDF...")
start_time = time.time()
response = requests.post(url, headers=headers, json=data)
end_time = time.time()

print(f"   Status: {response.status_code}")
print(f"   Processing Time: {end_time - start_time:.2f} seconds")
print(f"   Response Length: {len(str(response.json()))} characters")

if response.status_code == 200:
    answers = response.json().get('answers', [])
    print(f"   Number of Answers: {len(answers)}")
    for i, answer in enumerate(answers, 1):
        print(f"   Answer {i} Preview: {answer[:100]}...")
else:
    print(f"   Error: {response.text}")

print("\n" + "="*60)
print("✅ SUBMISSION TEST COMPLETE")
print("🚀 Your RAG service is READY for evaluation!")
print("="*60)
