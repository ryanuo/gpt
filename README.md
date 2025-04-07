# GPT API Project

This is a Flask-based API project that integrates multiple features, including AI text generation, image generation, and WeChat Official Account message processing.

## Features
- **AI Text Generation**: Supports generating text using different models.
- **Image Generation**: Generates images based on user input prompts.
- **WeChat Official Account Integration**: Handles messages and events from WeChat Official Accounts.

## Installation

1. Clone the project locally:
   ```bash
   git clone https://github.com/your-repo/gpt.git
   cd gpt
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Windows users, use venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   - Create a `.env` file and set the necessary environment variables, such as `WX_TOKEN`.

4. Install frontend dependencies (if needed):
   ```bash
   npm install
   ```

## Usage

1. Start the Flask application:
   ```bash
   python -m api.index
   ```

2. Access the following endpoints:
   - `http://localhost:5000/`: AI interface testing page.
   - `http://localhost:5000/image`: Image generation page.
   - `http://localhost:5000/models`: Retrieve the list of available models.

3. Deploy to Vercel:
   - Ensure the `vercel.json` configuration is correct.
   - Deploy using the Vercel CLI:
     ```bash
     vercel
     ```

## File Structure
```
gpt/
├── api/
│   ├── config.py          # Configuration file
│   ├── gptapi/            # GPT-related logic
│   ├── post/              # Data processing module
│   ├── routes/            # Routing module
│   ├── templates/         # Frontend templates
│   └── utils.py           # Utility functions
├── .gitignore             # Git ignore file
├── package.json           # Node.js configuration file
├── requirements.txt       # Python dependencies
├── vercel.json            # Vercel configuration
└── README.md              # Project documentation
```

## Contribution
Feel free to submit Issues or Pull Requests to improve this project.

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
