# GPT
Custom GPT API

## Features
- Provides a conversation interface based on the GPT model.
- Supports WeChat Official Account message processing.
- Offers a web-based testing interface.
- Supports fetching content from a specified URL and generating summaries.

## Dependencies
- For Python dependencies, refer to the `requirements.txt` file.
- Node.js version requirement: 18.x.

## Instructions
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the Flask application:
   ```bash
   python -m api.index
   ```

3. Access the testing page:
   Open your browser and visit `http://localhost:5001`.

4. Configure WeChat Official Account:
   - Set the WeChat Official Account `Token` to `wxToken`.
   - Configure the server URL to point to the `/wechat` endpoint.

5. Use the AI API:
   - Get the list of models: `GET /models`
   - Generate conversation completion results: `POST /g4f/<model>`
   - Fetch content from a URL and generate a summary: `POST /ai-post`

## Notes
- Ensure the `.env` file contains the necessary environment variables.
- The default model is `gpt-4o-mini`, which can be modified in `api/config.py`.
