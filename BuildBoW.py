# 构建词袋模型

import pandas as pd
import jieba
from gensim import corpora, models, similarities
import re
from collections import defaultdict
from scipy import sparse


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
	output: 无直接输出，在函数中生成词袋矩阵后直接保存为BoWmatrix.npz
'''
def Build_BoW(Datas):
	try:
		base_words= []
		text= []
		# 生成停用词列表
		with open('cn_stopwords.txt', 'r+') as stop:
			stopword= stop.read().split('\n')
		# 对文本进行分词
		for data in Datas:
			base_word= []
			doc= data['text']
			doc= re.sub(r'\d', '', doc)
			doc= re.sub(r'\n', '', doc)
			doc= re.sub(r'\s', '', doc)
			word_list= jieba.lcut(doc)
			for word in word_list:
				if word not in stopword:
					base_word.append(word)
			base_words.append(base_word)
		# 生成词典并且保存
		# 导出词典时用：dict = corpora.Dictionary.load('dic.dict')
		dictionary= corpora.Dictionary(base_words)
		# print(dictionary)
		dictionary.save('dic.dict')
		# 利用词典生成语料库
		corpus= []
		for word in base_words:
			corpus.append(dictionary.doc2bow(word))
		# 创建词袋矩阵
		word_num= len(dictionary.token2id.keys())
		text_num= len(Datas)
		row= []
		col= []
		data= []
		num= 0
		for i in corpus:
			for j in i:
				row.append(num)
				col.append(j[0])
				data.append(j[1])
			num+= 1
		# 矩阵的保存用到了scipy包中的sparse重的coo_matrix
		# coo_matrix保存时仅保存矩阵中不为0的数值以及位置
		# 导出矩阵时使用：sparse_matrix = scipy.sparse.load_npz('sparse_matrix.npz')
		coo_mat = sparse.coo_matrix((data, (row, col)), shape=(text_num, word_num))
		sparse.save_npz('BoWmatrix.npz', coo_mat)
		return ''
	except:
		return ''

def main():
	Datas= importData('Deduplicated_Data.txt')
	Build_BoW(Datas)

main()
