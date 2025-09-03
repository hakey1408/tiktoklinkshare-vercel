from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/fetch-real-ttlink')
def fetch_real_ttlink():
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

# Vercel expects a handler called 'app'
handler = app
# This is for local debug on intellij
#if __name__ == "__main__":
#    app.run(debug=True)