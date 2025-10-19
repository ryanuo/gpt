# GPT Interaction and Application Platform

[![中文][zh-src]][zh-href]
[![English][en-src]][en-href]

[zh-src]: https://img.shields.io/badge/中文-black.svg
[zh-href]: ./README.zh-CN.md
[en-src]: https://img.shields.io/badge/English-black.svg
[en-href]: ./README.md

## Project Overview

This is a Flask-based web application that provides API endpoints and a simple front-end interface for interacting with GPT models. Users can chat with AI, generate images, or get content summaries via a WeChat official account or web interface.

## Key Features
- **Text conversation with GPT models**: Supports multi-turn conversations for human-like chat experiences.
- **Image generation from user input**: Generate high-quality images using AI models.
- **WeChat official account message handling**: Supports auto-replies, image generation, and other features.
- **Content summarization**: Extract key information from long texts or web pages and generate concise summaries.
- **Custom AI service providers**: Supports custom AI providers, including OpenAI-compatible APIs.

## Usage

### Environment Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ryanuo/gpt.git
   cd gpt
   ```
   
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:

   ```bash
   cp .env.example .env
   ```

4. Start the service:

   ```bash
   python -m api.index
   ```

### Environment Variables

| Variable Name      | Description                                                            | Example Value                         | Required         | Notes                                                                           |
| ------------------ | ---------------------------------------------------------------------- | ------------------------------------- | ---------------- | ------------------------------------------------------------------------------- |
| `WX_TOKEN`         | WeChat official account token, used for message signature verification | `wechat_token_123456`                 | Yes (for WeChat) | Only needed if using WeChat message handling                                    |
| `OPENAI_API_KEY`   | API key for GPT models                                                 | `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` | No               | Required when using a custom OpenAI-compatible API (`PROVIDER=custom`)          |
| `PROVIDER`         | Specify AI service provider type                                       | `custom`                              | No               | Default is empty (uses `g4f` client default). `custom` means using a custom API |
| `COMPLETION_MODEL` | Default text generation model                                          | `gpt-4o-mini`, `gpt-3.5-turbo`        | No               | Defaults to `default_model` in `api/config.py` (`gpt-4o-mini`)                  |
| `API_KEY`          | Authentication key for custom AI service                               | `custom_api_key_789`                  | No               | Required if `PROVIDER=custom`, similar to `OPENAI_API_KEY`                      |
| `API_URL`          | API endpoint URL for custom AI service (OpenAI-compatible)             | `https://api.example.com/v1`          | No               | Required if `PROVIDER=custom`, defaults to OpenAI official API                  |

### Additional Notes

* Environment variables should be configured in the project root `.env` file (referenced in `.gitignore` to prevent leaks).
* Example setups:

  * Using default `g4f` service: no need to set `PROVIDER`, `API_KEY`, `API_URL`; optionally set `COMPLETION_MODEL`.
  * Using a custom API: set `PROVIDER=custom`, `API_KEY`, `API_URL`; optionally set `COMPLETION_MODEL`.

## API Endpoints

| API Type                    | Path              | Method | Parameters                                                                                                                                                                                                                                    | Response                                                                                                                              |
| --------------------------- | ----------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Conversation**            | `/g4f/<model>`    | POST   | - `message`: user input text<br>- `context` (optional): conversation context (format `[{"role":"user","content":"xxx"},{"role":"assistant","content":"xxx"}]`)<br>*Note: Model specified via `<model>` path; available models via `/vmodels`* | JSON containing `response` field (model-generated reply)                                                                              |
| **Image Generation**        | `/generate-image` | POST   | - `prompt`: description of the image (e.g., "Cyberpunk city night scene")<br>*Note: uses `flux` model*                                                                                                                                        | JSON containing `image_url` field (URL to access generated image)                                                                     |
| **WeChat Official Account** | `/wechat`         | POST   | Automatically parses WeChat server push messages (includes `signature`, `timestamp`, `nonce`, XML content, etc.)<br>*Note: uses default model in `api/config.py`, `gpt-4o-mini` by default*                                                   | Returns XML message reply according to WeChat specifications (text or rich media with image URLs)                                     |
| **Content Summarization**   | `/ai-post`        | POST   | - `url`: URL of webpage to summarize (e.g., `https://example.com/article`)<br>*Note: uses default model in `api/config.py`, `gpt-4o-mini` by default*                                                                                         | JSON containing `summary` field (concise summary of key content, ~50-200 words)                                                       |
| **Model List**              | `/vmodels`        | GET    | None<br>*Note: returns only supported model list, no model invocation*                                                                                                                                                                        | JSON grouped by type, e.g.:<br>`{ "GPT Series": ["gpt-4o-mini", "gpt-3.5-turbo"], "Other Models": ["claude-3-haiku", "gemini-pro"] }` |

## References

* [wechatpy Documentation](https://wechatpy.readthedocs.io/)
* [OpenAI GPT Models](https://github.com/xtekky/gpt4free)

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE.md) for details.
