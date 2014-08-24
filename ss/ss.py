__author__ = 'Administrator'
# coding=utf-8
import requests
import re
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
def get_html():

	# 构造requests header, 照抄就行
	s = requests.session()
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:27.0) Gecko/20100101 Firefox/27.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept': 'Language: zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
		'Accept': 'Encoding: gzip, deflate',
	}
	# 要提交的数据
	postdata = {
		'log': 'tttwwy',
		'pwd': 'xiaose123',
		'wp-submit': '登录',
		'redirect_to': 'http://yuikira.com/wp-admin/',
		'testcookie': '1'
	}

	# 登录页面地址
	url = 'http://yuikira.com/wp-login.php'

	# 请求页面
	r = s.get(url, headers=headers,timeout=5)

	# 保存cookies , 因为post数据时要将cookie传回
	cookies = dict(r.cookies)
	# print cookies
	# 登录, 提交数据
	r = s.post(url, headers=headers, cookies=cookies, data=postdata,timeout=5)

	cookies = dict(r.cookies)

	r = s.get('http://yuikira.com/lists/', headers=headers,cookies=cookies,timeout=5)

	return r.text

def get_server_list(html):
	server_list = []
	for item in re.findall(r"^\{[\s\S]*?\}",html,re.M):
		item = eval(item)
		print item
		server_list.append("proxy = ss://aes-256-cfb:{0[password]}@{0[server]}:{0[server_port]}".format(item))
	return server_list

try:
	html = get_html()
	# print html
	server_list = get_server_list(html)
	assert(len(server_list) > 0)

	print server_list
	result = ""
	with open("rc.txt","r") as f:
		flag = False
		for line in f:
			if not re.search("proxy.{0,3}=.{0,3}ss:.*",line):
				result += line
		for server in server_list:
			result += server + "\n"

	with open("rc.txt","w") as f:
		f.write(result)
	print "update successful"
finally:
	os.system('taskkill /im cow.exe')
	os.system("cow-hide.exe")
	print "run cow"
