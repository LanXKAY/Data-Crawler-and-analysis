import jieba
import re
from gensim import corpora, models, similarities

Number= 0

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
	para: Words需要去重的文本，为一个列表，列表中的元素为字典，且每一个元素代表一条文本
		  Start去重的文本开始的编号
	output: 无输出，去重后的文本直接写入一个新的txt文件

	本次试验实际上运行了两次该py文件
	第一次运行时为了更好的效果每一次只调用200条文本的集合进行去重操作，最后剩下大约1900条
	第二次直接把剩下的文本直接全部导入该函数进行操作，最后剩余约600条文本
'''
def Deduplicate(Words, Start):
	try:
		base_items= []
		# 生成停用词列表
		with open('cn_stopwords.txt', 'r+') as stop:
			stopword= stop.read().split('\n')
		# print(stopword)
		# 对文本分别进行分词
		for item in Words:
			base_item= []
			# 分词前对文本进行预处理
			doc = re.sub(r'\d', '', item['text'])
			doc = re.sub(r'\n', '', item['text'])
			doc = re.sub(r'\s', '', item['text'])
			word_list= jieba.lcut(doc)
			for word in word_list:
				if word not in stopword:
					base_item.append(word)
			base_items.append(base_item)
		# print(base_items)
		# 生成词典
		dictionary = corpora.Dictionary(base_items)
		# (dictionary)
		# 通过doc2bow稀疏向量生成语料库
		corpus = [dictionary.doc2bow(item) for item in base_items]
		# print(corpus)
		# 通过TF模型算法，计算出tf值
		tfidf = models.TfidfModel(corpus)
		# 通过token2id得到特征数（字典里面的键的个数）
		num_features = len(dictionary.token2id.keys())
		# 计算稀疏矩阵相似度，建立一个索引
		index = similarities.MatrixSimilarity(tfidf[corpus], num_features=num_features)
		# 计算各文本的相似性，得到相似值的矩阵Sim
		Sim= []
		for sentences in Words:
			compare_words = jieba.lcut(sentences['text'])
			compare_vec = dictionary.doc2bow(compare_words)
			sims= index[tfidf[compare_vec]]
			Sim.append(list(sims))
		dimension= len(Sim)
		for i in range(dimension):
			Sim[i][i]= 0
		# print(Sim)
		# 遍历矩阵，查找相似值大于0.1的文本对
		compares= []
		for i in range(dimension):
			for j in range(dimension):
				if(Sim[i][j]>= 0.15 and i<j):
					compares.append([i, j])
		# 合并匹配对，得到的结果为一个元素为列表的列表
		Similars_set= []
		Similars_list= []
		for i in compares:
			flag= 0
			for similar in Similars_set:
				if((i[0] in similar) or (i[1] in similar)):
					similar.add(i[0])
					similar.add(i[1])
					flag= 1
					break
			if(flag== 0):
				Similars_set.append(set(i))
		for i in Similars_set:
			ilist= list(i)
			Similars_list.append(ilist)
		# 整理匹配的文本对，最终得到一个包含需要删除的文本的编号列表
		delet= []
		for similar in Similars_list:
			for i in range(1, len(similar)):
				delet.append(similar[i])
		# print(delet)

		# 将清洗后的文本写入新的txt文件中
		# 定义了个全局变量以便在写入文件时对文本进行编号
		global Number
		with open('Deduplicated_Data.txt', 'a+') as f:
			for sentences in Words:
				if ((int(sentences['num'])-Start-1) not in delet):
					f.write(str(Number)+ '¥¥¥¥¥¥'+ sentences['time']+ '¥¥¥¥¥¥'+ sentences['text']+ '¥¥¥¥¥¥'+ sentences['degree'])
					Number+= 1
					print(Number)
					# print(sentences['num'])
				# f.write('\n')
		return ''
	except:
		return ''

def main():
	'''
	Words= importwords('Raw_data.txt')
	# 第一次运行该文件时
	# 每次处理200条文本
	start= 0
	end= 199
	while(end!= 7999):
		words= Words[start: end]
		Deduplicate(words, start)
		start+= 200
		end+= 200
	'''

	# 第二次去重时
	Words= importData('Deduplicated_Data1.txt')
	Deduplicate(Words, 0)

main()