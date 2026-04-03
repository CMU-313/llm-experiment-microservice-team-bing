import os
# Use Ollama library to interact with model:
import ollama
from ollama import chat, ChatResponse, Client
from langdetect import detect

# Get OLLAMA_HOST, if specified, or default to localhost:11434.
OLLAMA_URL = os.getenv("OLLAMA_HOST", "localhost:11434")

# Initialize the OpenAI client
client = Client(host=OLLAMA_URL)

MODEL_NAME = "llama3.2"  # Smallest Llama model for maximum speed

# Mapping from language codes to English names for common languages
LANG_CODE_TO_NAME = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'zh': 'Chinese',
    'ja': 'Japanese',
    'ko': 'Korean',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ar': 'Arabic',
    'hi': 'Hindi',
}

def get_language(post: str) -> str:
    try:
        code = detect(post)
        lang = LANG_CODE_TO_NAME.get(code)
        if lang:
            return lang
        else:
            # Unknown code, fallback to LLM
            return get_language_llm(post)
    except:
        # Detection failed, fallback to LLM
        return get_language_llm(post)

def get_language_llm(post: str) -> str:
    response = client.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": f"Detect the language of this text and reply with the English name only: {post}"
            }
        ],
        options={"temperature": 0.0, "num_predict": 10}  # Minimize randomness and limit output length
    )
    return response.message.content

def get_translation(post: str, lang: str) -> str:
    response = client.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": f"Translate this {lang if lang else 'given'} text to English. If it's gibberish, return just the post: \"{post}\""
            }
        ],
        options={"temperature": 0.0}  # Deterministic responses
    )
    return response.message.content

def translate_content(content: str) -> tuple[bool, str]:
    # Detect language first using fast library
    lang = get_language(content)
    
    # Only translate if not English
    if lang.lower() == "english":
        return (True, content)
    
    # Translate if non-English
    translation = get_translation(content, lang)

    return (False, translation)
