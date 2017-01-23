import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
import traceback
import socks
import socket
import requests
from urllib.parse import urljoin
import os
from shutil import copyfileobj
from urllib.parse import urlparse, ParseResult
import datetime
import logging
from bs4 import BeautifulSoup
import re 


scrapping_path = '/home/wesam/datasets/Scraping_Result_22_01_2017/'
error_scraping_path = '/home/wesam/datasets/Scraping_Result_22_01_2017/errors.txt'
data_set_path = '/home/wesam/datasets/Onion_Dataset/{0}/{0}.html'

if not os.path.exists(scrapping_path):
    os.mkdir(scrapping_path)
    
def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

tor_server = str('127.0.0.1')
tor_port = int('9050')
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, tor_server, tor_port)

# patch the socket module
socket.socket = socks.socksocket
socket.create_connection = create_connection


ext_list = ['jpg', 'png', 'gif', 'jpeg']

with open('white_list.txt') as f:
    white_list = f.readlines()


f_error = open(error_scraping_path, 'a', encoding='utf-8')

for file in white_list:
    print (file)
    links_list = []
    try:
        with open (data_set_path.format(file.strip()),'r', encoding='utf-8' , errors='ignore') as ins:
            txt= ' '.join(ins.readlines())    
    except Exception as e:
        print ('exception in ', file, e)
        continue

    soup = BeautifulSoup(txt, 'html.parser')
    
    for link in soup.findAll("a"):
        try:
            href = link['href']
            if href.lower()[-3:] in ext_list:
                links_list.append (href)
        except Exception:
            continue 

    for link in soup.findAll("img"):
        try:            
            href = link['src']
            if href.lower()[-3:] in ext_list:
                links_list.append (href)
        except:
            continue
    links_list =  list(set(links_list))
    if len(links_list)>0:
        if not os.path.exists(scrapping_path + file ):
            os.makedirs(scrapping_path + file)
            #print ( len(links_list),file  )
            for imgUrl in links_list:
                try:   
                    if urlparse(imgUrl).netloc=='':
                        imgUrl =urljoin(file, imgUrl)
                    imgName= scrapping_path + file + '/'+ imgUrl.split('/')[-1]
                    if not os.path.exists(imgName):
                        with urlopen(imgUrl, timeout=1) as in_stream, open(imgName, 'wb') as out_file:
                            copyfileobj(in_stream, out_file)                    
                except Exception:
                    f_error.write('{0}\t{1}\t{2}\n'.format(file, imgName, imgUrl))
                    continue
        else:
            continue