from flask import Flask, request, jsonify
from chatbot import chatbot_response

app = Flask(__name__)


@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.json
    question = data.get("question")
    
    # when the question missed
    if not question:
        return jsonify({"error": "Please provide a question."}), 400
    
    response = chatbot_response(question)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)