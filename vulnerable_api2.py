from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# index.html 서빙
@app.route('/')
def serve_html():
    return send_from_directory('.', 'index2.html')

# 인증 없이 config 정보 조회 가능 (GET)
@app.route('/api/v1/config', methods=['GET'])
def config():
    return jsonify({"config": "db_config_data", "version": "1.2.3"}), 200

# 명령어 실행 (Command Injection 시뮬레이션) (POST)
@app.route('/api/v1/exec_cmd', methods=['POST'])
def exec_cmd():
    data = request.get_json()
    cmd = data.get('cmd', '')

    try:
        result = os.popen(cmd).read()
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8443, ssl_context='adhoc')
