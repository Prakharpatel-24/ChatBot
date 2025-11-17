from openai import OpenAI
import time
import random

# Initialize client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

# Define models to rotate through
MODELS = [
    "deepseek/deepseek-r1:free",
    "meta-llama/llama-3.3-8b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
]

# Keep conversation context
chat_history = [{"role": "system", "content": "You are a helpful AI assistant."}]

def get_response(prompt):
    """Try each model until one succeeds"""
    for model in MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=chat_history + [{"role": "user", "content": prompt}],
                extra_headers={
                    "HTTP-Referer": "https://example.com",
                    "X-Title": "Dynamic AI Chat"
                }
            )
            return model, response.choices[0].message.content

        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "rate-limited" in error_msg.lower():
                print(f"⚠️ Model {model} is rate-limited. Trying next model...")
                time.sleep(1)
                continue
            else:
                print(f"Error with {model}: {error_msg}")
                continue
    return None, "All models are currently busy or unavailable."

# Interactive chat loop
print("🤖 Chat with AI (type 'exit' to quit)\n")
while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    model_used, reply = get_response(user_input)
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": reply})

    print(f"🧠 [{model_used}] → {reply}\n")
