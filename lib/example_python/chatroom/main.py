from hackdb import HackDB
from flask import Flask, request, jsonify

db = HackDB(token="", base_url="https://condor-willing-buck.ngrok-free.app/api/sdk/v1")

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
    
    try:
        message = {
            "content": data['message'],
            "timestamp": "now()"
        }
        db.messages.create(message)
        return jsonify({"status": "Message sent"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500 