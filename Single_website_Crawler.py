#!/usr/bin/python
import requests
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
from nltk_module import english_stopword_list
import time


class URLData: #URL 크롤링 결과 데이터 객체
    def __init__(self):
        self.wordFrequency_dict = dict()
        self.totalWord = 0
        self.URL = str()
        self.caculateTime = 0.0
        self.url_status = 0
        
    
    

#URLData Object --> Dictonary(convertible to JSON) and return it
def jsonify_URLData(URLData_parameter):
    py_dictionary = {}
    py_dictionary["wordFrequency_dict"] = URLData_parameter.wordFrequency_dict
    py_dictionary["totalWord"] = URLData_parameter.totalWord
    py_dictionary["URL"] = URLData_parameter.URL
    py_dictionary["caculateTime"]=URLData_parameter.caculateTime
    py_dictionary["url_status"]=URLData_parameter.url_status

    return py_dictionary



def word_englishParser(word):   #특수문자/숫자가 섞인 문자에서 영단어만 뽑아옵니다.
    engWord_list = []           #return engWord_list <List> 
    word = list(word)
    left = 0
    right = 0

    for ch in word:
        if not ch.isalpha():
            if left == right:
                left += 1
                right += 1
            else:
                engWord_list.append(''.join(word[left:right]))
                right += 1
                left = right
        else:
           right += 1
               
    if left != right:
           engWord_list.append(''.join(word[left:right]))


    return engWord_list
    




def analyze_URL_words(URL):     #받은 URL을 분석하여 단어 빈도수를 딕셔너리를 만듭니다.
    websiteData = URLData()     #return  dictonarized_URLData()<URLData<Dict, int, str, double, bool>>
    websiteData.URL = URL
 
    executeTime_start = time.time()

    #1. URL 유효성 검사
    try:
        websiteRequest_receiver = requests.get(URL)
    except:
        #작동하지 않거나 이상한 URL 집어 넣으면
        #실패 status를 담고 있는 빈 Dictonary를 반환합니다.
        websiteData.url_status = 1    # Faliure Flag = 1
        return jsonify_URLData(websiteData)

    #2. URL 중복 검사
    from elastic_module import search_urlMatch
    if (search_urlMatch(URL) == True):
        #중복 URL임이 발견 되면
        #중복 status를 담고 있는 빈 Dictonary를 반환합니다.
        websiteData.url_status = 2    # Duplicate Flag = 2
        return jsonify_URLData(websiteData)


    #HTML 원문 저장
    website_HTMLText = BeautifulSoup(websiteRequest_receiver.content, 'html.parser')
  

    #HTML에서 태그 부분을 버리고 문자열로 변환
    raw_string = website_HTMLText.find_all(recursive=False)
    wordList = []

    for rawPartition in raw_string:
        wordPartition = rawPartition.get_text()
        wordList.extend(wordPartition.split())


    #loop마다 한 단어 처리
    for word in wordList:
        word = word.lower()
        englishWord_list = []

        if not word.isalpha():
            #단어가 영단어가 아닌 경우 : 문자 단위로 탐색 부분적이라도 있으면 포함 
            englishWord_list = word_englishParser(word)
        else:
            englishWord_list = [word]
           
        

        for engWord in englishWord_list:
            if engWord in english_stopword_list:   #단어가 Stopword면 딕셔너리에 올라가지 않음
                continue
            if websiteData.wordFrequency_dict.get(engWord) == None:
                websiteData.wordFrequency_dict[engWord] = 1  #처음 등장한 단어는 등재하고
            else:
                websiteData.wordFrequency_dict[engWord] += 1 #이미 있던 단어는 count 추가!
                websiteData.totalWord += 1
    
    websiteData.caculateTime = time.time() - executeTime_start    #크롤링 시간 측정
    



    return jsonify_URLData(websiteData)
    


    
