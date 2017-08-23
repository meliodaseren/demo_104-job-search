import socks  # PySocks
import socket
from urllib.request import urlopen
import requests

# http://kissg.me/2016/06/02/not-a-tutorial-on-crawler/
# http://nladuo.github.io/2016/07/17/python%E4%B8%AD%E4%BD%BF%E7%94%A8tor%E4%BB%A3%E7%90%86/
# https://github.com/webfp/tor-browser-selenium

socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)  # tor 9150 port
socket.socket = socks.socksocket

# print(urlopen("http://icanhazip.com").read())
# icanhazip = requests.get("http://icanhazip.com").text
# print(icanhazip)

httpbinip = requests.get("https://httpbin.org/ip").text
print(httpbinip)
