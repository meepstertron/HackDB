from hackdb import HackDB
from flask import Flask, request, jsonify, render_template

db = HackDB(token="hkdb_tkn_065d8c41-4f5d-4678-a48c-ca26fb55808c", base_url="https://condor-willing-buck.ngrok-free.app/api/sdk/v1")

app = Flask(__name__)

@app.route('/messages', methods=['GET'])
def get_messages():
    """
    Get all messages from the chatroom.
    """
    try:
        messages = db.messages.find_many(limit=40)
        return jsonify(messages), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    

@app.route('/send', methods=['POST'])
def send_message():
    """
    Send a message to the chatroom.
    """
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error": "Message content is required"}), 400
    
    if 'name' not in data:
        data['name'] = "Anonymous"
    
    try:
        message = {
            "content": data['message'],
            "timestamp": "now()",
            "author": data.get('name', 'Anonymous'),
        }
        db.messages.create(message)
        return jsonify({"status": "Message sent"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500 
    
    
    
@app.route('/')
def index():
    """
    Serve the main chatroom page.
    """
    return render_template('index.html')

@app.route('/chat')
def chat():
    """
    Serve the chatroom page.
    """
    # send welcome message using username in query params
    username = request.args.get('name', 'Anon')
    if username:
        welcome_message = {
            "content": f"Welcome to the chatroom, {username}!",
            "timestamp": "now()",
            "author": "System"
        }
        db.messages.create(welcome_message)
    return render_template('chat.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)