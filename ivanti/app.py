# -*- coding: utf-8 -*-
import subprocess
from flask import Flask, request, jsonify, render_template
from urllib.parse import unquote

app = Flask(__name__)

# --------------------------------------
# 1. 로그인 페이지
# --------------------------------------
@app.route('/')
def home():
    return render_template('ivanti.html')  # 로그인 폼 HTML 필요

# --------------------------------------
# 2. 로그인 처리
# --------------------------------------
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    otp = request.form.get('otp')
    if username == 'admin' and password == 'password' and otp == '123456':
        return 'Logged in as admin!'
    return 'Login Failed.'

# --------------------------------------
# 3. 관리자 페이지
# --------------------------------------
@app.route('/admin')
def admin():
    return 'Admin page: Only logged-in users should see this.'

# --------------------------------------
# 4. 명령 실행 웹 UI (/command)
# --------------------------------------
@app.route('/command', methods=['GET', 'POST'])
def command_page():
    output = ''
    command = ''

    if request.method == 'POST':
        command = request.form.get('command')
    elif request.method == 'GET':
        command = request.args.get('cmd')

    if command:
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            output = result.decode('utf-8', errors='ignore')
        except subprocess.CalledProcessError as e:
            output = e.output.decode('utf-8', errors='ignore')
        except Exception as ex:
            output = "에러 발생: {}".format(str(ex))

    return render_template('command.html', output=output)

# --------------------------------------
# 5. API 명령 실행 (POST 방식)
# --------------------------------------
@app.route('/api/exec_cmd', methods=['POST'])
def exec_cmd():
    cmd = request.get_json().get('cmd', '')
    print(f"[📥 POST 명령 실행 요청] cmd = {cmd}")
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return jsonify({"result": result}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": e.output}), 500

# --------------------------------------
# 6. CVE 스타일 GET RCE (쿼리 키 없이 명령 직접 실행)
# 예: /api/v1/license/keys-status?whoami
# --------------------------------------
@app.route('/api/v1/license/keys-status', methods=['GET'])
def license_keys_status():
    raw_query = request.query_string.decode('utf-8')
    if not raw_query:
        return jsonify({"error": "No command provided"}), 400

    cmd = unquote(raw_query)  # URL 디코딩 처리
    print(f"[🚨 명령 실행] {cmd}")

    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return jsonify({"result": result}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": e.output}), 500

# --------------------------------------
# Flask 실행
# --------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=('vpn.fighting.co.kr+1.pem', 'vpn.fighting.co.kr+1-key.pem'), debug=True)
