# _*_ coding: utf-8 _*_
# # 抓取网页
# import urllib.request
# response = urllib.request.urlopen('http://php.net/')
# html = response.read()
# # print(html)
import json
import os
from bs4 import BeautifulSoup
# load data
def load(name):
    with open(name,encoding='UTF-8') as json_file:
        data = json.load(json_file)
        return data
# store data
def store(data):
    with open('./clean_texts/clean_texts.json','w') as json_file:
        json_file.write(json.dumps(data))

# compute term frequency
def computeTF(wordDict,doc):
    tfDict = {}
    docCount = len(doc) # 每个文章中单词数
    for word, count in wordDict.items():
        tfDict[word] = count/float(docCount)
    return tfDict

# compute Inverse Document Frequency
def computeIDF(docList):
    import math
    idfDict = {}
    N = len(docList)
    idfDict = dict.fromkeys(docList[0].keys(),0)
    for doc in docList:
        for word, val in doc.items():
            if val > 0:  # 不统计未出现的词
                idfDict[word] += 1
    for word, val in idfDict.items():
        idfDict[word] = math.log10(N/float(val))
    return idfDict
# compute TF-IDF
def computeTFIDF(tfBow, idfs):
    tfidf = {}
    for word, val in tfBow.items():
        tfidf[word] = val * idfs[word]
    return tfidf


if __name__ == "__main__":
    # 加载数据
    name = 'demo.json'
    datas = load(name)
    # 将抓取的网页转换为干净的文本
    # soup = BeautifulSoup(datas['contentHtml'], 'html5lib')
    # texts = soup.get_text(strip=True)
    texts = [BeautifulSoup(text['contentHtml'],'html5lib').get_text(strip=True) for text in datas]
    # titles = [title['title'] for title in datas]
    # print(texts)
    # # save data
    # if not os.path.exists('./clean_texts'):
    #     os.makedirs('./clean_texts')
    # dict = {}
    # for i in range(len(texts)):
    #     dict[titles[i]] = texts[i]
    # store(dict)
    # 将文本分词
    docList = []
    wordSet = set()
    for text in texts:
        docList.append(text.split())
        wordSet = wordSet.union(set(text.split()))
    # 删除停止词，例如：the, a, an, of 等
    # load stopword  获取英文停止词
    stopword = set(load('stopword.json'))
    wordSet = wordSet - stopword  # 剔除停止词

    # 词频统计
    docDicts = []  # 以字典型记录文档中单词出现的次数
    tfDicts = []  # 以字典型统计每篇文章中各单词的词频
    for doc in docList:
        wordDict = dict.fromkeys(wordSet, 0)
        for word in doc:
            if word in wordSet:
                wordDict[word] += 1
        tfDict = computeTF(wordDict, doc)
        docDicts.append(wordDict)
        tfDicts.append(tfDict)

    # print(tfDicts[0])

    # import pandas as pd
    # list = pd.DataFrame(wordDicts)
    # print(list)

    # 逆文档频率
    idfs = computeIDF(docDicts)
    # print(idf)

    # compute tf-idf
    tfidfs = []
    for docdict in docDicts:
        tfidf = computeTFIDF(docdict, idfs)
        tfidfs.append(tfidf)
    import pandas as pd
    print(pd.DataFrame(tfidfs))




