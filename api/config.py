from os import getenv


provider = getenv("PROVIDER", 'g4f') # options: g4f, custom
default_model = getenv('COMPLETION_MODEL', 'auto')
url = getenv("API_URL", "https://api.openai.com/v1")
api_key = getenv("API_KEY")
wx_token = getenv("WX_TOKEN", "default_wxToken")
ai_post_mode = getenv("AI_POST_MODE", "g4f") # options: g4f, static
default_model_url = f"{url}/models"
api_url = f"{url}/chat/completions"

def is_custom_provider():
    return provider == 'custom'

def is_static_mode():
    return ai_post_mode == 'static'