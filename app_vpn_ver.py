# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, render_template_string, jsonify
import subprocess
from subprocess import Popen, PIPE
import requests

app = Flask(__name__)

# 로그인 실패 시 HTML
fail_page = """
<!DOCTYPE html>
<html>
<head>
    <title>로그인 실패</title>
    <style>
        body { text-align: center; font-family: sans-serif; margin-top: 100px; }
        h1 { color: red; }
    </style>
</head>
<body>
    <h1>❌ 로그인 실패!</h1>
    <p>아이디, 비밀번호, OTP를 확인해주세요.</p>
</body>
</html>
"""

# 홈: 로그인 화면
@app.route('/')
def home():
    return render_template('ivanti.html')

# 로그인 처리
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    otp = request.form['otp']

    # 클라이언트 IP 자동 추출
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    print(f'[+] 로그인 시도 from {client_ip} - ID: {username}')

    if username == 'admin' and password == 'password' and otp == '123456':
        try:
            # 클라이언트 VPN Agent로 연결 요청
            url = f"http://{client_ip}:8800/connect_vpn"
            print(f"[+] VPN 연결 요청: {url}")
            res = requests.post(url, timeout=3)
            print(f"[+] 클라이언트 응답: {res.text}")
        except Exception as e:
            print(f"[X] VPN 연결 요청 실패: {str(e)}")

        return render_template_string(open('portal.html', encoding='utf-8').read())
    else:
        return render_template_string(fail_page)

# 관리자 페이지
@app.route('/admin')
def admin():
    return 'Admin page: Only logged-in users should see this.'

# 실습용 RCE 유사 엔드포인트 (CVE 참고)
@app.route('/api/hidden', methods=['POST'])
def hidden():
    command = request.form.get('command')
    if not command:
        return 'No command received.'

    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return "Command output:\n{}".format(result)
    except subprocess.CalledProcessError as e:
        return "Error executing command:\n{}".format(e.output)

# 명령어 실행 웹페이지
@app.route('/command', methods=['GET', 'POST'])
def command_page():
    output = ''
    if request.method == 'POST':
        command = request.form.get('command')
        if command:
            try:
                result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                output = result.decode('euc-kr', errors='ignore')
            except subprocess.CalledProcessError as e:
                output = e.output.decode('utf-8', errors='ignore')
            except Exception as ex:
                output = "에러 발생: {}".format(str(ex))
    return render_template('command.html', output=output)

# 인증 없이 접근 가능한 RCE 실습용 (CVE-2024-21887 유사)
@app.route('/api/v1/license/keys-status', methods=['GET'])
def keys_status():
    query = request.args.get("query", "")
    try:
        process = Popen(query, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        result = stdout.decode() + stderr.decode()
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 클라이언트 IP 확인
@app.route('/whoami')
def whoami():
    return f'당신의 IP: {request.remote_addr}'

# HTTPS로 실행 (인증서 포함)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8443, ssl_context=('vpn.fighting.co.kr+2.pem', 'vpn.fighting.co.kr+2-key.pem'), debug=True)
