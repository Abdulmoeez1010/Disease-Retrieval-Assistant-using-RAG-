import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Test 1: Check if key is loaded
api_key = os.getenv("GEMINI_API_KEY")
print("=" * 50)
print("TEST 1: API Key Loading")
print("=" * 50)
if api_key:
    print(f"✅ API Key found")
    print(f"   First 20 chars: {api_key[:20]}...")
    print(f"   Length: {len(api_key)} characters")
    print(f"   Has spaces: {' ' in api_key}")
    has_quotes = ('"' in api_key) or ("'" in api_key)
    print(f"   Has quotes: {has_quotes}")
else:
    print("❌ API Key NOT found!")
    print("\nCheck:")
    print("1. Is your .env file in the same directory as this script?")
    print("2. Is it named exactly '.env' (not .env.txt)?")
    exit()

# Test 2: Try direct Google AI SDK
print("\n" + "=" * 50)
print("TEST 2: Google AI SDK")
print("=" * 50)
try:
    import google.generativeai as genai
    genai.configure(api_key=api_key.strip())  # Strip any whitespace
    
    print("✅ SDK configured successfully")
    
    # List models
    print("\nAvailable models:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"  ✓ {m.name}")
    
    # Test generation
    print("\nTesting generation...")
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Say 'Hello World'")
    print(f"✅ Response: {response.text}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nThis means either:")
    print("1. Your API key is invalid")
    print("2. Your API key is revoked")
    print("3. You need to enable the Gemini API")

# Test 3: Try LangChain wrapper
print("\n" + "=" * 50)
print("TEST 3: LangChain Wrapper")
print("=" * 50)
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=api_key.strip()
    )
    
    result = llm.invoke("Say 'Hello from LangChain'")
    print(f"✅ LangChain works: {result.content}")
    
except Exception as e:
    print(f"❌ LangChain Error: {e}")