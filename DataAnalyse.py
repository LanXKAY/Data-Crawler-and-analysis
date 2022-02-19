import jieba
from gensim import corpora, models, similarities
import re
import numpy as np
from numpy import linalg
import array
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
	output: TFIDF计算得到的TFIDF矩阵
'''
def ComputeTFIDF(Datas):
	try:
		base_words= []
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
		# 生成词典
		dictionary= corpora.Dictionary(base_words)
		# 利用词典生成语料库
		corpus= []
		for word in base_words:
			corpus.append(dictionary.doc2bow(word))
		# 使用TFidfModel方法生成tfidf模型
		tfidf= models.TfidfModel(corpus)
		# 通过模型计算文本的TFIDF特征值
		word_tf_tdf= list(tfidf[corpus])
		# print(len(word_tf_tdf))
		# 建立TFIDF矩阵，同样使用了coo_mat矩阵方法
		word_num = len(dictionary.token2id.keys())
		text_num= len(Datas)
		row= []
		col= []
		data= []
		num= 0
		for i in word_tf_tdf:
			for j in i:
				row.append(num)
				col.append(j[0])
				data.append(j[1])
			num+= 1
		coo_mat = sparse.coo_matrix((data, (row, col)), shape=(text_num, word_num))
		# print(coo_mat)
		# 将稀疏矩阵coo_mat转化成numpy的array类型并且返回
		TFIDF= coo_mat.toarray()
		return TFIDF
	except:
		return ''

'''
	para: TFIDF通过前面函数计算得到的TFIDF矩阵，numpy中的array类型
	output: Down_TFIDF降维后的TFIDF矩阵，numpy中的array类型
'''
def SVD(TFIDF, percentage):
	try:
		# 调用numpy中的方法对TFIDF矩阵进行SVD分解
		U,Sigma,VT= linalg.svd(TFIDF)
		# 计算需要截断（降维）的位置
		Sum= np.sum(Sigma)
		sum= 0
		percentage= np.zeros(len(Sigma))
		for i in range(len(Sigma)):
			sum += Sigma[i]
			percentage[i] = sum/Sum
			if(percentage[i]>= percentage):
				cut = i+1
				break
		# 降维操作
		Sigma[cut:] = 0
		S= np.zeros(TFIDF.shape)
		S[:len(Sigma), :len(Sigma)]= np.diag(Sigma)
		Down_TFIDF = np.dot(np.dot(TFIDF.T, U), S)
		return Down_TFIDF
	except:
		return ''

def main():
	Datas= importData('Deduplicated_Data.txt')
	TFIDF= ComputeTFIDF(Datas)
	print('TFIDF矩阵为：')
	print(TFIDF)
	print(TFIDF.dtype, TFIDF.shape)
	Down_TFIDF= SVD(TFIDF, 0.9)
	print(Down_TFIDF)
	return ''

main()