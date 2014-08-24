# coding=utf-8
__author__ = 'Administrator'
import HTMLParser
import urlparse
import urllib
import urllib2
import cookielib
import string
import re
import sys
import os
import ss
reload(sys)
sys.setdefaultencoding("utf-8")

#登录的主页面
hosturl = 'http://yuikira.com/wp-login.php'
#post数据接收和处理的页面（我们要向这个页面发送我们构造的Post数据）
posturl = 'http://yuikira.com/wp-login.php'

#设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)

#打开登录主页面（他的目的是从页面下载cookie，这样我们在再送post数据时就有cookie了，否则发送不成功）
h = urllib2.urlopen(hosturl)

#构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
           'Referer' : 'ttp://yuikira.com/wp-login.php'}
#构造Post数据，他也是从抓大的包里分析得出的。
postData = {'log' : 'tttwwy',
            'pwd' : 'xiaose123',
            'wp-submit' : '登录',
            'redirect_to' : 'http://yuikira.com/wp-admin/',
            'testcookie' : '1'

            }

#需要给Post数据编码
postData = urllib.urlencode(postData)

#通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程
request = urllib2.Request(posturl, postData, headers)
# print request

html =  urllib2.urlopen("http://yuikira.com/lists/").read()

server = ""
for item in re.findall(r"^\{[\s\S]*?\}",html,re.M):
    item = eval(item)
    # print item
    server += "proxy = ss://aes-256-cfb:{0[password]}@{0[server]}:{0[server_port]}\n".format(item)

result = ""
with open("rc.txt","r") as f:
    flag = False
    for line in f:
        if re.search("proxy.{0,3}=.{0,3}ss:.*",line):
            if not flag:
                result += server
                flag = True
        else:
            result += line
    if not flag:
        result += server

with open("rc.txt","w") as f:
    f.write(result)

print "update successful"
os.system('taskkill /im cow-hide.exe')
os.system("cow-hide.exe")
print "run cow"




