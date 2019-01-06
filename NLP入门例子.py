
# 抓取网页
import urllib.request
response = urllib.request.urlopen('http://php.net/')
html = response.read()
# print(html)

# 将抓取的网页转换为干净的文本
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'html5lib')
text = soup.get_text(strip=True)
# print(text)

# 将文本分词
tokens = [t for t in text.split()]
# print(tokens)

# 词频统计
import nltk
freq =  nltk.FreqDist(tokens) # 返回字典
# for key, val in freq.items():
#     print(str(key)+':'+str(val))

#绘制词频图形
freq.plot(20,cumulative=False)

# 删除停止词，例如：the, a, an, of 等

# 获取英文停止词
from nltk.corpus import stopwords
stopwords.words('english')

# # 命令行运行如下命令，获取stopwords资源
# import nltk
# nltk.download('stopwords')

# 复制一个列表，对列表中的标记进行遍历，并删除其中的停止词
clean_tokens = tokens[:]
sr = stopwords.words('english')
for token in tokens:
    if token in sr:
        clean_tokens.remove(token)

freq = nltk.FreqDist(clean_tokens)
# for key,val in freq.items():
#     print(str(key)+":"+str(val))
freq.plot(20,cumulative=False)

