#使用LDA模型对数据进行聚类处理

import jieba
import jieba.posseg as jp
from gensim import corpora, models, similarities
import re

new_words= ['新冠', '肺炎', '新冠肺炎']

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
			dict= {'num': seg[0], 'time': seg[1], 'text': seg[2]}
			Datas.append(dict)
		return Datas
	except:
		return ''

'''
	para: Datas一个列表，列表的内容为字典每一个字典表示一条谣言
	output: 无直接输出,聚类得到的结果直接输出至DataCluster
	使用LDA模型对数据进行聚类，这是一个概率模型，输出为某一条文本最有可能属于的类别
'''
def LDA(Datas):
	try:
		base_words= []
		text= []
		# 生成停用词列表
		with open('cn_stopwords.txt', 'r+') as stop:
			stopword= stop.read().split('\n')
		# 添加新词
		for i in new_words:
			jieba.add_word(i)
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
		# 生成稀疏向量集合
		corpus= []
		for word in base_words:
			corpus.append(dictionary.doc2bow(word))
		# LDA模型，num_topics设置聚类数，即最终主题的数目
		lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=15)
		# 展示每个主题前五的词语
		# 推断每个语句的所属的主题类别
		# 结果直接输出至DataCluster.txt中
		with open('DataCluster.txt', 'a+') as f:
			for topic in lda.print_topics(num_words=5):
				f.write(str(topic))
				f.write('\n')
			f.write('\n\n\n')
			for e, values in enumerate(lda.inference(corpus)[0]):
				topic_val = 0
				topic_id = 0
				for tid, val in enumerate(values):
					if val > topic_val:
						topic_val = val
						topic_id = tid
				temp= str(topic_id)+ '->'+ Datas[e]['text']
				f.write(temp)
				f.write('\n')
		return ''
	except:
		return ''

def main():
	Datas= importData('Deduplicated_Data.txt')
	LDA(Datas)
	return ''

main()
