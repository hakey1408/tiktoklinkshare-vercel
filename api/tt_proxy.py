from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://hakey1408.github.io"])  # Restrict CORS to specific origins

ALLOWED_REFERERS = ["https://hakey1408.github.io"]

@app.before_request
def restrict_to_fetch_real_ttlink():
    if request.path != '/fetch-real-ttlink':
        return jsonify({'error': 'Unauthorized'}), 401
    return None

@app.route('/fetch-real-ttlink')
def fetch_real_ttlink():
    # Check Referer header
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