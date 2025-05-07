from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def serve_html():
    return send_from_directory('.', 'index.html')

@app.route('/api/v1/configuration', methods=['GET'])
def config():
    if request.headers.get('X-AUTH-TOKEN') != 'valid-token':
        return jsonify({"error": "unauthorized"}), 401
    return jsonify({"config": "internal stuff"})

@app.route('/api/v1/unauthenticated-access', methods=['GET'])
def backdoor():
    return jsonify({"config": "bypassed authentication"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8443, ssl_context='adhoc')
