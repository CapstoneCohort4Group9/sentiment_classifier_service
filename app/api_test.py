#!/usr/bin/env python3
import urllib.request
import urllib.parse
import json
import sys

# Update this URL to your deployed Fargate service
BASE_URL = "http://localhost:8095"  # Change this to your deployed URL

def test_health():
    try:
        url = f"{BASE_URL}/health"
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            print(f"Health check: {response.status}")
            print(f"Response: {data}")
            print()
            return response.status == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_sentiment(text):
    try:
        url = f"{BASE_URL}/analyze_sentiment"
        payload = {"text": text}
        data = json.dumps(payload).encode('utf-8')
        
        req = urllib.request.Request(
            url,
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            print(f"Text: '{text}'")
            print(f"Status: {response.status}")
            print(f"Sentiment: {result['sentiment']}")
            print(f"Confidence: {result['confidence']:.3f}")
            return True
            
    except urllib.error.HTTPError as e:
        print(f"Text: '{text}'")
        print(f"HTTP Error: {e.code}")
        print(f"Error: {e.read().decode()}")
        return False
    except Exception as e:
        print(f"Text: '{text}'")
        print(f"Request failed: {e}")
        return False
    finally:
        print("-" * 50)

def main():
    print("Testing Sentiment API...")
    print(f"Target URL: {BASE_URL}")
    print("=" * 50)
    
    # Test health endpoint first
    if not test_health():
        print("❌ Health check failed - stopping tests")
        sys.exit(1)
    
    # Test various sentiments
    test_cases = [
        "I love this product! It's amazing!",
        "This is terrible and doesn't work.",
        "The weather is okay today.",
        "Best purchase ever! Highly recommend!",
        "Worst experience of my life.",
        "The book was informative and well-written.",
        ""  # Edge case: empty text
    ]
    
    passed = 0
    total = len(test_cases)
    
    for text in test_cases:
        if test_sentiment(text):
            passed += 1
    
    print(f"Tests completed: {passed}/{total} passed")
    if passed == total:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()