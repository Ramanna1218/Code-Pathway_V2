import os
import openai
from flask import Flask, request, jsonify, render_template, send_from_directory
from dotenv import load_dotenv, find_dotenv
from flask_cors import CORS  # Import CORS

# Initialize Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')

# Apply CORS to allow all origins or specify your frontend domain
CORS(app)

# Load environment variables from .env file
load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return render_template('Main.html')

@app.route('/Lesson<int:lesson_number>.html')
def lesson(lesson_number):
    return render_template(f'Lesson{lesson_number}.html')

# Route to evaluate the user's code using OpenAI's GPT API
@app.route('/evaluate_answer', methods=['POST'])
def evaluate_answer():
    data = request.get_json()

    # Validate incoming data
    user_code = data.get('code')
    current_question = data.get('question')
    if not user_code:
        return jsonify({'feedback': 'No code provided. Please submit your solution.'}), 400

    # Construct the prompt for evaluation
    prompt = (
        f"You are speaking directly to a student, here is the quiz question: {current_question} "
        f"Student code:\n{user_code}\n"
        "Provide feedback on whether their code is correct, say 'correct' at the very beginning if they are right. Give examples on how the users code can improve. Do not give the answer away if the user code is wrong."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful coding tutor."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.2
        )

        feedback = response['choices'][0]['message']['content'].strip()
        return jsonify({'feedback': feedback})
    except openai.error.AuthenticationError:
        return jsonify({'feedback': 'Authentication error. Please check your API key.'}), 401
    except Exception as e:
        return jsonify({'feedback': f'Error processing request: {str(e)}'}), 500
    
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

