# -*- coding: utf-8 -*-
import subprocess
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 홈: 로그인 화면 보여주기
@app.route('/')
def home():
    return render_template('ivanti.html')

# 로그인 처리
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    otp = request.form['otp']

    # 아주 간단한 로그인 체크 (진짜 로그인 아님)
    if username == 'admin' and password == 'password' and otp == '123456':
        return 'Logged in as admin!'
    else:
        return 'Login Failed.'

# 관리자만 접근할 수 있는 페이지
@app.route('/admin')
def admin():
    return 'Admin page: Only logged-in users should see this.'

# 취약한 엔드포인트 (실습용)
@app.route('/api/hidden', methods=['POST'])
def hidden():
    command = request.form.get('command')
    if not command:
        return 'No command received.'

    # 위험하지 않게 출력만!
    try:
        # 실제 명령어 실행
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return "Command output:\n{}".format(result)
    except subprocess.CalledProcessError as e:
        return "Error executing command:\n{}".format(e.output)

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

if __name__ == '__main__':
    app.run(debug=True)
