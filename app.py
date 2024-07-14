import os
import openai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import requests
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Create an assistant
assistant = openai.beta.assistants.create(
    name="Custom Assistant",
    instructions="You are a helpful assistant. Use the provided tools to gather information when necessary.",
    tools=[{
        "type": "function",
        "function": {
            "name": "get_internal_data",
            "description": "Get data from internal API",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query to search for in the internal API"
                    }
                },
                "required": ["query"]
            }
        }
    }],
    model="gpt-3.5-turbo-0613"
)

def get_internal_data(query):
    # This is a mock function. In a real scenario, you would call your internal API here.
    internal_api_url = "https://your-internal-api.com/data"
    try:
        response = requests.get(f"{internal_api_url}?query={query}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error calling internal API: {e}")
        return {"error": "Failed to retrieve data from internal API"}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    thread_id = request.json.get('thread_id')
    
    try:
        # Create a thread if it doesn't exist
        if not thread_id:
            thread = openai.beta.threads.create()
            thread_id = thread.id
        
        # Add a message to the thread
        openai.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
        )
        
        # Run the assistant
        run = openai.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant.id
        )
        
        # Wait for the run to complete
        while True:
            run = openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if run.status == 'completed':
                break
            elif run.status == 'requires_action':
                for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                    if tool_call.function.name == "get_internal_data":
                        query = json.loads(tool_call.function.arguments)['query']
                        output = get_internal_data(query)
                        openai.beta.threads.runs.submit_tool_outputs(
                            thread_id=thread_id,
                            run_id=run.id,
                            tool_outputs=[{
                                "tool_call_id": tool_call.id,
                                "output": json.dumps(output)
                            }]
                        )
        
        # Get the assistant's response
        messages = openai.beta.threads.messages.list(thread_id=thread_id)
        assistant_response = messages.data[0].content[0].text.value
        
        return jsonify({'response': assistant_response, 'thread_id': thread_id})
    
    except openai.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return jsonify({'error': 'An error occurred while processing your request'}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
