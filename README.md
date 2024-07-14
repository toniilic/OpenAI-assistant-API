# OpenAI Assistant API Proof of Concept

This project demonstrates a basic implementation of OpenAI's Assistant API with a Flask web application. It includes features such as maintaining conversation threads and integrating with an internal API.

## Prerequisites

- Python 3.7+
- pip
- OpenAI API key

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/openai-assistant-poc.git
   cd openai-assistant-poc
   ```

2. Install dependencies:
   ```
   pip install openai flask python-dotenv requests
   ```

3. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

4. Create a `templates` folder and add an `index.html` file for the frontend.

## Running the Application

1. Start the Flask server:
   ```
   python app.py
   ```

2. Open a web browser and navigate to `http://localhost:5000` to interact with the assistant.

## Features

- Conversation threading
- Integration with internal API (mocked in this example)
- Error handling for API calls and unexpected errors

## Customization

- Modify the `get_internal_data` function to integrate with your actual internal API.
- Adjust the assistant's instructions and tools in the `openai.beta.assistants.create` call.
- Customize the frontend in `templates/index.html` to fit your needs.

## Security Notes

- Never commit your `.env` file or expose your API keys.
- Implement proper authentication and rate limiting for production use.

## License

This project is licensed under the MIT License.
