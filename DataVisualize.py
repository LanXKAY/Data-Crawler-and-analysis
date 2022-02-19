#对数据进行可视化处理

import jieba
import re
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt

'''
	para: FilePath需要读取的文件名
	output: Datas一个列表，列表的内容为字典每一个字典表示一条谣言
			字典内容包括编号num，发布时间time，谣言文本text，发布者信用等级degree
'''
def importData(FilePath):
	try:
		datas= []
		Datas= []
		with open(FilePath, 'r') as f:
			for line in f.readlines():
				datas.append(line)
		for data in datas:
			seg= data.split('¥¥¥¥¥¥')
			dict= {'num': seg[0], 'time': seg[1], 'text': seg[2], 'degree': seg[3]}
			Datas.append(dict)
		return Datas
	except:
		return ''

'''
	para: Datas一个列表，列表的内容为字典每一个字典表示一条谣言
		  KeyWordList一个列表，列表的内容为需要搜索的关键词
	output: result一个列表，列表的内容为字典，每一个字典表示一条表示关键词的文本
'''
def KeyWordListSearch(Datas, KeyWordList):
	result= []
	for data in Datas:
		doc= data['text']
		doc= re.sub(r'\d', '', doc)
		doc= re.sub(r'\n', '', doc)
		doc= re.sub(r'\s', '', doc)
		word_list= jieba.lcut(doc)
		# 通过关键词对文本进行搜索
		for i in KeyWordList:
			if i in doc:
				result.append(data)
				break
	return result

'''
	para: Datas一个列表，列表的内容为字典每一个字典表示一条谣言
	output: counter一个字典，字典的值分别为对应的时间段里谣言的个数
	该函数对找到的和疫情有关的谣言进行处理，具体处理方法为根据发布时间进行计数
	以14天为组对日期进行分组并分别计数，时间跨度为2020.1.23-2020.5.14
'''
def AboutEpidemic(Datas):
	EpidemicList=  {'新冠', '肺炎', '武汉', '疫情', '医护', '医疗', '感染', '确诊'}
	AboutEpidemicList= KeyWordListSearch(Datas, EpidemicList)
	# 使用到了datetime类来进行日期的计算
	FirstDate= datetime(2020, 1, 23)
	Distance= []
	for i in AboutEpidemicList:
		date= datetime.strptime(i['time'], '%Y-%m-%d %H:%M:%S')
		Days= (date-FirstDate).days
		# 结合疫情发生的时间，舍去2020.1.23之前的与关键词有关的谣言
		if(Days>=0):
			Distance.append(int(Days/14))
	counter= Counter(Distance)
	counter= dict(counter)

	return counter

'''
	para: Datas一个列表，列表的内容为字典每一个字典表示一条谣言
	output: counter一个字典，字典的值分别为对应的时间段里谣言的个数
	该函数对找到的和美国有关的谣言进行处理，具体处理方法为根据发布时间进行计数并统计
	以半年为一个组，时间跨度为2017.1.1-2020.5.27
'''
def AboutAmerica(Datas):
	AmericaList= {'美国', '美帝', '特朗普', '纽约'}
	AboutAmericaList= KeyWordListSearch(Datas, AmericaList)
	FirstDate= datetime(2017, 1, 1)
	Distance= []
	for i in AboutAmericaList:
		date= datetime.strptime(i['time'], '%Y-%m-%d %H:%M:%S')
		Days= (date-FirstDate).days
		Distance.append(int(Days/183))
	counter= Counter(Distance)
	counter= dict(counter)

	return counter

'''
	para: Datas一个列表，列表的内容为字典每一个字典表示一条谣言
	output: dic一个字典，字典的key为3个degree，对应的value为该degree包含的人数
	该函数统计并计算所有谣言发布者的信用等级
'''
def SummarizeDegree(Datas):
	DegreeList= []
	for i in Datas:
		DegreeList.append(i['degree'])
	counter= Counter(DegreeList)
	counter= dict(counter)
	dic= {'middle': 0, 'normal': 0, 'small': 0}
	# 对key值进行处理，便于后期饼图的绘画
	for i in counter:
		if(i=='中\n'):
			dic['middle']= counter[i]
		elif(i== '正常\n'):
			dic['normal']= counter[i]
		else:
			dic['small']= counter[i]
	return dic

'''
	para: dicdate一个字典，里面包含绘图的数据
		  x_label一个列表，当需要更换x轴坐标的名称时选用，若不用时设为0
		  title一个字符串，条形图的名称
		  heng条形图的形状，若为0则表示垂直条形图，取1则表示水平条形图
	output: 无直接输出，但绘图后会直接显示
	该函数利用dicdate中的数据绘制条形图
'''
def dict2plot(dicdate, x_label= 0, title, heng= 0):
	by_value= []
	for i in sorted(dicdate):
		temp= (i, dicdate[i])
		by_value.append(temp)
	x= []
	y= []
	for d in by_value:
		x.append(d[0])
		y.append(d[1])

	if heng == 0:
		plt.bar(x, y)

		plt.xlabel('Time')
		plt.ylabel('Nums')
		plt.title(title)

		if(x_label!=0):
			plt.xticks(x, x_label, rotation= 45)
		plt.show()
		return

	elif heng == 1:
		plt.barh(x, y)
		plt.xlable('Time')
		plt.ylabel('Nums')
		plt.title(title)

		if(x_label!=0):
			plt.xticks(x, x_label, rotation= 45)
		plt.show()
		return

	else:
		return 'Error'

'''
	para: dicdate绘图用到的数据
		  title饼图的名称
	output: 无直接输出，但绘图后会直接显示
	该函数使用dicdate中的数据绘制饼状图
'''
def dic2pie(dicdate, title):
	#计算饼状图的各比例
	sum= 0
	for i in dicdate:
		sum+= dicdate[i]
	for i in dicdate:
		dicdate[i]= dicdate[i]/sum
	labels= []
	sizes= []
	for i in dicdate:
		labels.append(i)
		sizes.append(dicdate[i])
	explode= (0, 0.1, 0)

	plt.pie(sizes, explode= explode, labels= labels, autopct= '%1.1f%%', shadow= False, startangle= 90)
	plt.title(title)

	plt.show()
	return ''


def main():
	Datas= importData('Deduplicated_Data.txt')

	'''
	# 查找与疫情有关的内容
	dicdate= AboutEpidemic(Datas)
	time_list= ['1.23-2.5', '2.6-2.19', '2.20-3.4', '3.5-3.18', '3.19-4.1', '4.2-4.15', '4.16-4.29', '4.30-5.14']
	dict2plot(dicdate= dicdate, x_label= time_list, title= 'The nums of the weibo about epidemic', heng= 0)
	'''

	'''
	# 查找与美国有关的内容
	dicdate= AboutAmerica(Datas)
	time_list= ['1st half of 2017', '2nd half of 2017', '1st half of 2018', '2nd half of 2018', '1st half of 2019', '2nd half of 2019', '1st half of 2020']
	dict2plot(dicdate= dicdate, x_label= time_list, title= 'The nums of the weibo about America', heng= 0)
	'''

	# 总结统计发布谣言的人的信用等级
	dicdate= SummarizeDegree(Datas)
	dic2pie(dicdate, 'The Summarize of Degree')


main()
