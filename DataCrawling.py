import requests
import re
from bs4 import BeautifulSoup

start_url1= 'https://service.account.weibo.com/index?type=5&status=4&page='
start_url2= 'https://service.account.weibo.com'
headers= {'Cookie': 'login_sid_t=9665e520784e3bf1aa5f4ffe90e57e73; cross_origin_proto=SSL; _s_tentry=-; Apache=8854185835173.277.1589793826234; SINAGLOBAL=8854185835173.277.1589793826234; ULV=1589793827236:1:1:1:8854185835173.277.1589793826234:; SSOLoginState=1589961890; un=15910716653; wvr=6; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFwmefauUwNyh-JKxdVzSz25JpX5KMhUgL.Foq01h5ceo.ES0M2dJLoI7Ueqg4qCc84; ALF=1621920904; SCF=AkAp9mtw06GNQfwO423fm4_V4TKD0HiWFhMYT7IdzP0QetbdskRj5ZnyATR35bAJ14TQaKYKSVzCFdY9Z61-Yhw.; SUB=_2A25zzylJDeRhGeBN41IX8ifOzDuIHXVQvR2BrDV8PUNbmtANLVCtkW9NRAwXPBG89LMYlbBVL4kzgvh9Mr8A1Fcd; SUHB=0S7CE0u21wRkoM; UOR=,,login.sina.com.cn; webim_unReadCount=%7B%22time%22%3A1590391911194%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A42%2C%22msgbox%22%3A0%7D0'}

'''
	para: url网址
	output: demo网页的内容
'''
def gethtmltext(url):
	try:
		response= requests.get(url= url, headers= headers, timeout=30)
		demo= response.text.encode('utf-8').decode('unicode_escape')
		demo= demo.replace('\\/', '/')
		return demo
	except:
		return ''

'''
	para: html网页的文本
	output: rid谣言网页的网址列表
'''
def GetLink(html):
	try:
		rid= re.findall(r'><div class="m_table_tit" ><a href="(.*?)" target="_blank">', html)
		return rid
	except:
		return ''

'''
	parar: html网页的文本
	output: content谣言的正文部分
'''
def GetCon(html):
	try:
		soup = BeautifulSoup(html, 'xml')
		# 运用BeaurifulSopu以及正则表达式查找谣言的正文部分
		content=soup.find("div","part_report part_report_alone clearfix").find("div","W_main_half_r").find("div","item top").find("div","con")
		if(content.a!= None):
			if(content.find(text = '查看全文') == None):
				text = content.text
				pattern = re.compile("：(.*?)$", re.DOTALL)
				content =pattern.findall(text)[0]
			else:
				text = content.input.text
				pattern = re.compile("value=\'(.*?)\'", re.DOTALL)
				content = pattern.findall(text)[0]
		else:
			content = '无'
		# 对谣言文本的格式进行一些必要的处理
		content = content.replace('\n', '')
		content = content.replace('\t', '')
		content = content.replace('\u200b', '')
		return content
	except:
		return ''

'''
	para: html网页的文本
	output: time谣言的发布日期时间
'''
def GetTime(html):
	try:
		soup = BeautifulSoup(html, 'xml')
		content = soup.find('div', 'item top').find('p', 'publisher')
		text = content.text
		Time = re.findall(r"20\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", text)
		for i in Time:
			time = i
		return time
	except:
		return ''

'''
	para: html网页的文本
	output: degree发布者的信用等级
'''
def GetDegree(html):
	try:
		soup= BeautifulSoup(html, 'xml')
		# 通过BeautifulSoup查找谣言发布者的信用等级
		content= soup.find('div', 'W_main_half_r').find('p', 'mb W_f14').find('img', 'W_ico16 credit_middle')
		if(content!= None):
			degree= '中'
		else:
			content= soup.find('div', 'W_main_half_r').find('p', 'mb W_f14').find('img', 'W_ico16 credit_normal')
			if(content!= None):
				degree= '正常'
			else:
				degree= '低'
		return degree
	except:
		return ''

# 主函数
# depth为爬取的深度（页数）
def main():
	depth = 401
	num = 1
	for Num in range(1, depth):
		url=start_url1+ str(Num)
		html= gethtmltext(url)
		rid= GetLink(html)
		for i in rid:
			url = start_url2 + i
			html = gethtmltext(url)
			content = GetCon(html)
			time= GetTime(html)
			degree= GetDegree(html)
			# print(num)
			# 谣言内容的保存，通过'¥¥¥¥¥¥'进行分隔
			with open('Raw_data.txt', 'a+') as f:
				f.write(str(num)+ '¥¥¥¥¥¥'+ time+ '¥¥¥¥¥¥'+ content+ '¥¥¥¥¥¥'+ degree)
				f.write('\n')
			num += 1
	return ''

main()
