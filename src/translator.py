import os
# Use Ollama library to interact with model:
import ollama
from ollama import chat, ChatResponse, Client

# Get OLLAMA_HOST, if specified, or default to localhost:11434.
OLLAMA_URL = os.getenv("OLLAMA_HOST", "localhost:11434")

# Initialize the OpenAI client
client = Client(host=OLLAMA_URL)

MODEL_NAME = "llama3.1:8b"

def get_language(post: str) -> str:
    context = "You are a language classifier. Detect the language of the following text and reply only with the English name of the language:  "# TODO: Insert context
    # ---------------- YOUR CODE HERE ---------------- #
    response = client.chat(
        model=MODEL_NAME,  # model name
        messages=[
            {
                "role": "user",
                "content": context + post
            }
        ]
    )

    return response.message.content

# TODO: Implement Basic LLM integration
def get_translation(post: str) -> str:
    context = "You are a language translator. Detect the language of the following text and reply only with the English translation of the text. If you cannot detect a language, just return the input as is: "
    # ---------------- YOUR CODE HERE ---------------- #
    # Make a request to your Ollama model, running on your Colab server
    response = client.chat(
        model=MODEL_NAME,  # model name
        messages=[
            {
                "role": "user",
                "content": context + post
            }
        ]
    )

    return response.message.content

def translate_content(content: str) -> tuple[bool, str]:
    # Detect language first
    lang = get_language(content)
    
    # Only translate if not English
    if lang.lower() == "english":
        return (True, content)
    
    # Translate if non-English
    translation = get_translation(content)
    
    # This checks if the translation does not ONLY contain the translation, but also additional LLM text
    if ":'" in translation:
        translation = content

    return (False, translation)
