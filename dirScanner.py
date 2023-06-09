# zebra
# from subprocess import Popen, PIPE

import argparse
import threading
from random import choice
from urllib.error import HTTPError
from requests import Session
from bs4 import BeautifulSoup
#  for anonymity secure your device && for linux system you can delete this comment and exec code as below
#  def macchanger(iface):
#    Popen(cmd=['ifconfig', iface, down], stdin=PIPE, stdout=PIPE, stderr=PIPE)
#    Popen(cmd=['macchanger', '-r', iface], stdin=PIPE, stdout=PIPE, stderr=PIPE)
#    Popen(cmd=['ifconfig',iface, up], stdin=PIPE, stdout=PIPE, stderr=PIPE)
#
#
#  def clear_cache():
#    return Popen(cmd=['sync', '&&', 'echo', '1', '>', 'proc/sys/drop_caches'], stdin=PIPE, stdout=PIPE, stderr=PIPE)

TOR_SOCKS = {'http':'http://127.0.0.1:9050',
             'https':'https://127.0.0.1:9050'}

u_agent = [
    'AppleCoreMedia/1.0.0.17E8255 (iPhone; U; CPU OS 13_4 like Mac OS X; de_at)',
    'Mozilla/5.0 (Linux; Android 11; RMP2102 Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/109.0.5414.118 Safari/537.36 [FB_IAB/FB4A;FBAV/402.1.0.24.84;]',
    'Mozilla/5.0 (Linux; Android 11; RMX3085 Build/RP1A.200720.011) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.154 Mobile Safari/537.36 GNews Android/2022120648',
    'Mozilla/5.0 (Linux; Android 7.0; Comet) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; A80 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/106.0.5249.126 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/394.1.0.51.107;]',
    'Mozilla/5.0 (Linux; Android 9; SM-N950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36 [ip:93.32.152.208]',
    'Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.75 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/406.0.0.26.90;]',
    'Mozilla/5.0 (Linux; Android 11; CPH2135 Build/RKQ1.201217.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/109.0.5414.85 Mobile Safari/537.36 [FB_IAB/Orca-Android;FBAV/397.0.0.20.81;]',
    'Mozilla/5.0 (Linux; Android 13; SM-A037G Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.57 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/406.0.0.26.90;]',
    'Mozilla/5.0 (Linux; Android 9; I4113) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0'
    ]


def wordlist(path):
    try:
       fd = open(path, 'r')
       word = [i.rstrip() for i in fd.readlines()]
       return word
    except FileNotFoundError:
       print('Error file not found!')

class HTTPConnectionHandler:

      def __init__(self, url, path_wordlist, cookie=None):
          self.wordlist = wordlist(path_wordlist)
          self.conn = Session()
          self.url = url
          self.headers = {'User-Agent' : choice(u_agent)}
          self.cookie = cookie
          if self.cookie:
             self.headers['Cookie'] = self.cookie
          if self.url[-1] != '/':
             self.url += '/'
          self.conn.proxy = TOR_SOCKS

      def dirscanner(self):
            try:
               result = 0
               for path in self.wordlist:
                 url = self.url + path
                 reason = self.conn.get(url, allow_redirects=False, headers=self.headers)
                 if reason.status_code != 404:
                    print('[%d] %s'%(reason.status_code, reason.url))
                    result += 1
            except requests.exceptions.ConnectionError:
                 print('target not found! or please check your connection')

if __name__ == '__main__':
     parser = argparse.ArgumentParser(description="Python3 dirscanner, search web directory")
     parser.add_argument('-t',help='target url ',type=str)
     parser.add_argument('-c', help='cookie (optional)', type=str)
     parser.add_argument('-w', help='path wordlist', type=str)
     args = parser.parse_args()
     cookie = None
     if args.c:
          cookie = args.c
     conn = HTTPConnectionHandler(url=args.t,path_wordlist=args.w, cookie=cookie)
     conn.dirscanner()
