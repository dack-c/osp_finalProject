import nltk
from nltk.corpus import stopwords

#소스 파일 Initial Code
english_stopword_list = []      #English stopword list

if len(english_stopword_list) == 0:
    nltk.download('stopwords')
    for stopword in stopwords.words("english"):
        english_stopword_list.append(stopword)