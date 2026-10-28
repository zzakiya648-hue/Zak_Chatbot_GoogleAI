import json
import urllib.request

# 1. Configuration
# Paste your actual free Google Gemini API key here
GEMINI_API_KEY = "ENTER_YOUR_API_KEY_HERE"
API_URL = f"https://googleapis.com{GEMINI_API_KEY}"

print("🤖 Universal Gemini Chatbot initialized! Type 'quit' to exit.\n")

# 2. History Tracker
conversation_history = []

while True:
    user_input = input("You: ")
    
    if user_input.lower() == 'quit':
        print("Chatbot: Goodbye!")
        break
        
    if not user_input.strip():
        continue
        
    # Set up the conversation history array formatting structure
    conversation_history.append({"role": "user", "parts": [{"text": user_input}]})
    payload = {"contents": conversation_history}
    
    # Convert data into binary formats required by web servers
    json_data = json.dumps(payload).encode("utf-8")
    
    # Configure the standard web transmission headers
    req = urllib.request.Request(API_URL, data=json_data)
    req.add_header("Content-Type", "application/json")
    
    try:
        # 3. Open connection directly over the internet channel
        with urllib.request.urlopen(req) as response:
            response_data = json.loads(response.read().decode("utf-8"))
            
            # Navigate cleanly through the data layers to grab the text reply string
            bot_reply = response_data["candidates"][0]["content"]["parts"][0]["text"]
            print(f"\nChatbot: {bot_reply}\n")
            
            # Save history context logs
            conversation_history.append({"role": "model", "parts": [{"text": bot_reply}]})
            
    except urllib.error.HTTPError as e:
        error_message = e.read().decode("utf-8")
        print(f"\nServer Error ({e.code}): {error_message}\n")
        conversation_history.pop()  # Remove failed string element
    except Exception as e:
        print(f"\nAn error occurred: {e}\n")
