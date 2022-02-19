import pandas as pd
import jieba
import re


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
	output: 无直接输出，函数找到的特征结果直接用于建立DataFrame并且保存为Feature.csv
'''
def Feature_Extract(Datas):
	try:
		dict= {'单词数': [], '超链接': [], '带话题': [], '疫情相关': [], '信用等级': []}
		EpidemicList= {'新冠', '肺炎', '武汉', '疫情', '医护', '医疗', '感染'}
		for data in Datas:
			doc= data['text']
			#文本的预处理
			doc= re.sub(r'\d', '', doc)
			doc= re.sub(r'\n', '', doc)
			doc= re.sub(r'\s', '', doc)
			doc= re.sub(r'，', '', doc)
			doc= re.sub(r'。', '', doc)
			doc= re.sub(r'：', '', doc)
			word_list= jieba.lcut(doc)
			word_nums= len(word_list)
			IsWithHyperlink= ('http' in doc)
			IsWithTopic= ('#' in doc)
			Degree= data['degree']
			IsAboutEpidemic= False
			for word in EpidemicList:
				if word in doc:
					IsAboutEpidemic= True
					break
			dict['单词数'].append(word_nums)
			dict['超链接'].append(IsWithHyperlink)
			dict['带话题'].append(IsWithTopic)
			dict['疫情相关'].append(IsAboutEpidemic)
			dict['信用等级'].append(Degree)
		# 通过DataFrame存储文本的数值特征并保存
		# #保存DataFrame文件，读取时使用命令: pd.read_csv('Feature.csv')
		d= pd.DataFrame(dict)
		d.to_csv('Feature.csv', index_label= 'index_label')
		return ''
	except:
		return ''

def main():
	Datas= importData('Deducated_Data')
	Feature_Extract(Datas)

main()