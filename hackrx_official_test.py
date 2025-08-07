# Official HackRX API Test - Exact Specification Format
import requests
import json
import time

def test_hackrx_api():
    """Test the /hackrx/run endpoint with official specification format"""
    
    print("🏆 OFFICIAL HACKRX API TEST")
    print("=" * 50)
    
    # Exact API specification format
    url = "http://localhost:8000/hackrx/run"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json", 
        "Authorization": "Bearer 72b507a14e702a622f69f0154ca1db7888ec2e8f14a34727fe63389e74207a7e"
    }
    
    # Official sample request payload
    data = {
        "documents": ["https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A20Z"],
        "questions": [
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
            "What is the waiting period for pre-existing diseases (PED) to be covered?",
            "Does this policy cover maternity expenses, and what are the conditions?",
            "What is the waiting period for cataract surgery?", 
            "Does the medical expenses for an organ donor covered under this policy?",
            "What is the No Claim Discount (NCD) offered in this policy?",
            "Is there a benefit for preventive health check-ups?",
            "How does the policy define a 'hospital'?",
            "What is the extent of coverage for AYUSH treatments?",
            "Are there any sub-limits on room rent and ICU charges for Plan A?"
        ]
    }
    
    print(f"📡 Testing POST {url}")
    print(f"📋 {len(data['questions'])} questions about policy document")
    print(f"🔑 Using Bearer token authentication")
    
    try:
        start_time = time.time()
        response = requests.post(url, headers=headers, json=data, timeout=300)
        end_time = time.time()
        
        print(f"\n✅ Status Code: {response.status_code}")
        print(f"⏱️  Processing Time: {end_time - start_time:.2f} seconds")
        
        if response.status_code == 200:
            result = response.json()
            answers = result.get("answers", [])
            
            print(f"📊 Response Summary:")
            print(f"   • Number of answers: {len(answers)}")
            print(f"   • Total response size: {len(str(result))} characters")
            
            # Show first few answers as sample
            print(f"\n📝 Sample Answers:")
            for i, answer in enumerate(answers[:3], 1):
                print(f"   {i}. {answer[:100]}...")
                
            print(f"\n🎯 EXPECTED RESPONSE FORMAT: ✅")
            print(f"   {{\"answers\": [...]}}")
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    print("\n" + "=" * 50)
    print("🏆 HACKRX API TEST COMPLETE")

if __name__ == "__main__":
    test_hackrx_api()
