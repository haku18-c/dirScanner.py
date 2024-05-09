# ! /usr/bin/python3
# https://github.com/haku-16c/hakuscanner

from requests import Session
from requests import exceptions
from random import random
from math import ceil
from termcolor import colored
import threading
import re
import base64
import argparse
import time

def b64string(plaintext):
    plaintext = plaintext.encode('ascii')
    b64str = base64.b64encode(plaintext)
    b64str = b64str.decode('ascii')
    return b64str

def wordlist(path):
    opener = open(path, 'r').readlines()
    div = 0;
    if len(opener) % 2 == 0:
        div = 4
    else:
        div = 3
    result = []
    items = len(opener) // div
    for i in range(div):
        result.append(opener[(i*items):(i+1)*items])
    return result

class Handler:

      def __init__(self, url, path):
          self.url = url
          self.word = wordlist(path)
          self.conn = Session()

      def random_agent(self, path='dictionary/u_agent.txt'):
          f_agent = open(path, 'r').readlines()
          idx = ceil(random() * len(f_agent))
          self.conn.headers['User-Agent'] = f_agent[idx-1].rstrip()

      def tor(self):
          self.conn.proxies = {
                               'http':'socks5h://localhost:9050',
                               'https':'socks5h://localhost:9050'
                               }
      def getServer(self):
          _s = self.conn.get(self.url)
          if _s.headers['Server']:
              print('Server   : {}'.format(_s.headers['Server']))
#          if _s.headers['X-Powered-By']:
#              print('Platform : {}'.format(_s.headers['X-Powered-By']))


      def send(self, path):
          for i in path:
            self.random_agent()
            html = self.conn.get(self.url + i.rstrip(), allow_redirects=False)
            if(html.status_code != 404):
              if html.status_code < 300:
                 print(colored('[+]found => {}\t{}'.format(html.status_code, html.url), 'red'))
              elif html.status_code < 400:
                 print(colored('[+]found => {}\t{}'.format(html.status_code, html.url), 'blue'))

      def threadstart(self):
          threads = []
          print('starting attack to {}'.format(self.url))
          self.getServer()
          print('\n[+] CODE \tURL\n')
          for i in self.word:
             t = threading.Thread(target=self.send, args=(i,))
             threads.append(t)
          for i in threads:
             i.start()
          for i in threads:
             i.join()

def main():
    parser = argparse.ArgumentParser(description='haku web scanner tools')
    parser.add_argument('-t', metavar='Target', type=str, help='url target to scan')
    parser.add_argument('-w', metavar='W', type=str, default='dictionary/wordlist.txt', help='wordlist path')
    parser.add_argument('-timeout', metavar='timeout', type=int, required=False, help='timeout request')
    parser.add_argument('-tor', metavar='Tor Network', type=bool, help='using anonymous surfing')
    args = parser.parse_args()
    connector = Handler(args.t, args.w)
    connector.threadstart()

if __name__ == '__main__':
   main()
