import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # Load environment variables from .env file

api_key = os.getenv("open_api_key")  # Get the API key from environment variable

if not api_key:
    print("API key not found. Please set the 'open_api_key' in the .env file.")
    print("You can obtain an API key from https://platform.openai.com/account/api-keys")
    exit(1)

print("API key loaded successfully.")
client = OpenAI(api_key=api_key)

system_prompt = """
You are a helpful AI tutor.

Your job is to explain technical concepts
in a simple and beginner-friendly way with easy example explaining core concepts and edge cases.

Use examples whenever possible.

The user knows Python and basic machine learning.
"""

conversation_history = []

print("=" * 50)
print("        BASIC LLM CHATBOT")
print("=" * 50)
print("Type 'exit' to quit.")
print("Type 'clear' to clear conversation.")
print("=" * 50)


while True :
    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        print("Exiting the chatbot. Goodbye!")
        break
    if not user_input:
        print("Please enter a message.")
        continue
    if user_input.lower() == "clear":
        conversation_history.clear()
        print("Conversation history cleared.")
        continue

    conversation_history.append(
        {
            "role": "user",
           "content": user_input
        }
    )
    try:
        response = client.responses.create(
        model="gpt-5.6",
        instructions=system_prompt,
        input=conversation_history
        )
        
        assistant_response = response.output_text
        
        print("\nAI:", assistant_response)
        
        conversation_history.append({
            "role": "assistant",
            "content": assistant_response
        })

        
    except Exception as e:

        print("\nSomething went wrong.")
        print("Error:", e)

        # Remove the user message if request failed because we dont need contect which ai did not respond to
        conversation_history.pop()