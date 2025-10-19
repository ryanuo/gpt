from os import getenv


provider = getenv("PROVIDER", 'g4f') # options: g4f, custom
default_model = getenv('COMPLETION_MODEL', 'gpt-4o-mini')
url = getenv("API_URL", "https://api.openai.com/v1")
api_key = getenv("API_KEY")
wx_token = getenv("WX_TOKEN", "default_wxToken")
default_model_url = f"{url}/models"
api_url = f"{url}/chat/completions"

def is_custom_provider():
    return provider == 'custom'