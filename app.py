from flask import Flask, request, jsonify
from flask_cors import CORS
from lyric_generator import generate_lyrics

app = Flask(__name__)
CORS(app) 

@app.route('/generate_lyrics', methods=['POST'])
def get_lyrics():
    data = request.get_json()
    title = data.get('title', '')
    is_retry = data.get('is_retry', False)
    lyrics = generate_lyrics(title, is_retry)
    return jsonify({'lyrics': lyrics})

if __name__ == '__main__':
    app.run(port=5000) 