import time
from hackdb import HackDB
from flask import Flask, request, jsonify, render_template

db = HackDB(token="hkdb_tkn_7dd9d15b-924e-42c7-899b-d274730e5341", base_url="https://hackdb.hexagonical.ch/api/sdk/v1")

app = Flask(__name__)

global last_fetch, cache

last_fetch = time.time() - 31
cache = []

@app.route('/messages', methods=['GET'])
def get_messages():
    """
    Get all messages from the chatroom.
    """
    global last_fetch, cache  
    if last_fetch + 30 < time.time():
        try:
            messages = db.messages.find_many(limit=40)
            print(f"Fetched {len(messages)} messages from the database.")
            last_fetch = time.time()
            cache = messages
            return jsonify(messages), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify(cache), 200


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
        
        cache.append(message)
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