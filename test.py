# -*- code:utf-8 -*-
import redis
import re

# with open("/home/yu/Desktop/1234.txt", "w") as file:
    # file.write(b'\xc3\xbf\xc3\xbe2\\u00000\\u00001\\u00009\\u0000.\\u00003\\u0000.\\u00002\\u00007\\u0000\xc3\xaev\\u0007h\\r\\u0000\\n\\u0000\\u0000\xc2\x97Bl\\u001a\xc3\xbf\\r\\u0000\\n\\u0000\\t\\u00001\\u0000.\\u0000\xc2\x9e[\xc2\xb0s\\u0000N*NH\\u0000T\\u0000T\\u0000P\\u0000\\rg\xc2\xa1RhVv^\xc3\x91S\\u0001\xc2\x90Q\x7fu\xc2\x98\xc3\x99~Om\xc3\x88\xc2\x89hV\\r\\u0000\\n\\u0000\\t\\u00002\\u0000.\\u0000\xc2\x9e[\xc2\xb0s\\u0000N*Nh\xc2\x88US\xc3\x90c\xc2\xa4N\\rg\xc2\xa1RhV\\f\xc3\xbfv^\xc2\xb0\xc2\x8bU_\xc2\x85Q\xc2\xb9[\\u00020\\b\xc3\xbfg\\u0000e\\u0000t\\u0000 \\u0000a\\u0000n\\u0000d\\u0000 \\u0000p\\u0000o\\u0000s\\u0000t\\u0000\\t\xc3\xbf\\r\\u0000\\n\\u00002\\u00000\\u00001\\u00009\\u0000.\\u00003\\u0000.\\u00002\\u00008\\u0000\xc3\xaev\\u0007h\\r\\u0000\\n\\u0000\\u0000\xc2\x97Bl\\u001a\xc3\xbf\\r\\u0000\\n\\u0000\\t\\u00001\\u0000.\\u0000\xc2\x9e[\xc2\xb0s')

# FILE = os.open("/home/yu/Desktop/1234.txt", os.O_WRONLY|os.O_CREAT)
# os.write(FILE, b'\xc3\xbf\xc3\xbe2\\u00000\\u00001\\u00009\\u0000.\\u00003\\u0000.\\u00002\\u00007\\u0000\xc3\xaev\\u0007h\\r\\u0000\\n\\u0000\\u0000\xc2\x97Bl\\u001a\xc3\xbf\\r\\u0000\\n\\u0000\\t\\u00001\\u0000.\\u0000\xc2\x9e[\xc2\xb0s\\u0000N*NH\\u0000T\\u0000T\\u0000P\\u0000\\rg\xc2\xa1RhVv^\xc3\x91S\\u0001\xc2\x90Q\x7fu\xc2\x98\xc3\x99~Om\xc3\x88\xc2\x89hV\\r\\u0000\\n\\u0000\\t\\u00002\\u0000.\\u0000\xc2\x9e[\xc2\xb0s\\u0000N*Nh\xc2\x88US\xc3\x90c\xc2\xa4N\\rg\xc2\xa1RhV\\f\xc3\xbfv^\xc2\xb0\xc2\x8bU_\xc2\x85Q\xc2\xb9[\\u00020\\b\xc3\xbfg\\u0000e\\u0000t\\u0000 \\u0000a\\u0000n\\u0000d\\u0000 \\u0000p\\u0000o\\u0000s\\u0000t\\u0000\\t\xc3\xbf\\r\\u0000\\n\\u00002\\u00000\\u00001\\u00009\\u0000.\\u00003\\u0000.\\u00002\\u00008\\u0000\xc3\xaev\\u0007h\\r\\u0000\\n\\u0000\\u0000\xc2\x97Bl\\u001a\xc3\xbf\\r\\u0000\\n\\u0000\\t\\u00001\\u0000.\\u0000\xc2\x9e[\xc2\xb0s')
# str = "Host: 192.168.16.129:9999 \
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0 \
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8 \
# Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2 \
# Accept-Encoding: gzip, deflate \
# Referer: http://192.168.16.129:9999/ \
# Content-Type: multipart/form-data; boundary=---------------------------251862599328095 \
# Content-Length: 525 \
# Connection: keep-alive \
# Upgrade-Insecure-Requests: 1 \
# "
# str2 = ''
#
# res = re.search('Content-Type(.*)', str)
#
# print(res.group(1))

# print(b'form-data' in b'123form-data123')
str1 = b"\xe6\x96\xb0\xe5\xbb\xba\xe6\x96\x87\xe6\x9c\xac\xe6\x96\x87\xe6\xa1\xa3"
str2 = b" (3).txt"
print(len(str1))