from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, origins=["http://localhost:63342", "https://hakey1408.github.io"])  # Restrict CORS to specific origins

API_KEY = os.environ.get("API_KEY")  # Set this in Vercel environment variables
ALLOWED_REFERERS = ["https://hakey1408.github.io"]

@app.before_request
def restrict_to_fetch_real_ttlink():
    if request.path != '/fetch-real-ttlink':
        return jsonify({'error': 'Unauthorized'}), 401

@app.route('/fetch-real-ttlink')
def fetch_real_ttlink():
    # Authentication: Check API key
    client_api_key = request.headers.get("X-API-KEY")
    if not client_api_key or client_api_key != API_KEY:
        return jsonify({'error': 'Unauthorized'}), 401
    # Optional: Check Referer header
    referer = request.headers.get("Referer", "")
    if not any(referer.startswith(r) for r in ALLOWED_REFERERS):
        return jsonify({'error': 'Forbidden'}), 403
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing url parameter'}), 400
    try:
        response = requests.get(url, allow_redirects=False)
        location = response.headers.get('Location')
        purified_location = location.split('?')[0] if location else None
        return jsonify({
            'status': response.status_code,
            'locked-location': location,
            'purified-location': purified_location
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# This is for local debug on intellij
#if __name__ == "__main__":
#    app.run(debug=True)