
from math import sqrt, log10


def get_cosine_similarity_list(DictionaryList, targetURL):
    #Cosine Similiarity
    #input : DictonaryList와 비교 대상이 되는 targetURL - targetURL은 valid임이 보증됨
    #예를 들어 DictonaryList는 10의 길이를 지니고 DictonaryList[5]에 대한 코사인 유사도를 분석하는 것임
    #output : 유사도가 높은 순으로 정렬한 2개의 키(URL, cosine_similarity)를 지닌 딕셔너리 반환.
    
    #0. targetURL이 들어있는 DictionaryList 상의 index를 구합니다 (= pivot).
    pivot = 0
    for url_dictionary in DictionaryList:
        if (url_dictionary["URL"] == targetURL):
            break
        else:
            pivot += 1

    wordDictonaryList_length = len(DictionaryList)

    #1. pivot의 norm을 일단 구합니다.
    pivot_norm = 0
    for singleWord_frequency in DictionaryList[pivot]["wordFrequency_dict"].values():
        pivot_norm += singleWord_frequency ** 2
    
    pivot_norm = sqrt(pivot_norm)


    #2. Pivot을 제외한 List들과의 Cosine Similarity를 구하고 딕셔너리 쌍을 만들어 List에 추가함
    cosine_similarity_list = []
    for index in range(0, wordDictonaryList_length):
        if (index == pivot): #똑같은 URL끼리 비교 안함
            continue
        if (DictionaryList[index]["url_status"] != 0): #정상적이지 않은 URL은 분석 불가
            continue
        
        #URL, cosine_similarity 딕셔너리 쌍
        URL_cosine_dic = dict()
        URL_cosine_dic["URL"] = DictionaryList[index]["URL"]

        target_wordDictionary = DictionaryList[index]["wordFrequency_dict"]

        #2-1. 대상의 norm 구하기
        target_norm = 0
        for target_singleWord_frequency in target_wordDictionary.values():
            target_norm += target_singleWord_frequency ** 2
        
        target_norm = sqrt(target_norm)


        #2-2. pivot과 대상 간의 내적 구하기
        dot_product = 0
        for key, value in DictionaryList[pivot]["wordFrequency_dict"].items():
            #pivot에 있는 단어가, target에도 있으면 내적 값(dot_product)에 곱을 더해준다.
            if (key in target_wordDictionary):
                dot_product += value * target_wordDictionary[key]

        #2-3. cosine_similarity 값을 딕셔너리에 저장
        URL_cosine_dic["cosine_similarity"] = float(dot_product) / (pivot_norm * target_norm)

        #2-4. 딕셔너리 리스트에 추가
        cosine_similarity_list.append(URL_cosine_dic)

    
    #3. 유사도가 높은 순으로 정렬
    cosine_similarity_list.sort(reverse = True, key = lambda dic: dic["cosine_similarity"])


    return cosine_similarity_list





def get_top_TFIDF_list(DictionaryList, targetURL):
    #get Top TFIDF of targetURL List
    #input : DictionaryList, targetURL
    #output : Top TFIDF List of [word, TF-IDF] List

    #key : word   value : [word count in doc1, word count in doc2 ...]를 이루는 딕셔너리
    combined_wordFrequency_dict = dict()
    
    #1. DictionaryList에서 유효한 URL을 담고 있는 인덱스만 추가합니다.
    validIndex_list = []
    targetURL_index = 0  #Dictionary에서 value 리스트에서 targetURL이 가리키는 인덱스값 
    for idx in range(0, len(DictionaryList)):
        if (DictionaryList[idx]["url_status"] == 0): #정상 상태이면
            validIndex_list.append(idx)
            if (DictionaryList[idx]["URL"] == targetURL):
                targetURL_index = len(validIndex_list)-1
        
    #2. combined_wordFrequency_dict 작성
    for idx in range(0, len(validIndex_list)):
        #유효한 URL의 딕셔너리를 선형 탐색
        search_wordFreq_dict = DictionaryList[validIndex_list[idx]]["wordFrequency_dict"]

        for key in search_wordFreq_dict.keys():
            if (key in combined_wordFrequency_dict):
                continue  #이미 탐색된 단어이면 통과
            
            #새로운 단어에 대응하는 Value list 생성
            combined_wordFrequency_dict[key] = []

            #Ex) 3번 문서(idx = 2)에서 처음 발견된 단어이면, 1~2번 문서엔 그 단어를 가지고 않음은 당연합니다.
            for indexBefore in validIndex_list[0:idx]:
                combined_wordFrequency_dict[key].append(0)
            
            #Ex) 3번 ~ 끝 문서에서는 해당 단어 갯수를 찾아 입력합니다.
            for indexAfter in validIndex_list[idx:]:
                if (key in DictionaryList[indexAfter]["wordFrequency_dict"]):
                    combined_wordFrequency_dict[key].append(DictionaryList[indexAfter]["wordFrequency_dict"][key])
                else:
                    combined_wordFrequency_dict[key].append(0)
    

    #3. combined_dict에 각 문서의 총 단어 수를 나누면 TF가 됩니다.
    for key in combined_wordFrequency_dict.keys():
        for valueIndex in range(0, len(validIndex_list)):
            combined_wordFrequency_dict[key][valueIndex] /= DictionaryList[validIndex_list[valueIndex]]["totalWord"]
    

    #4. IDF을 구한 뒤 TF(combined_dict)에 곱하면
    # combined_dict 값은 TF-IDF 가 됩니다.
    documentCount = len(validIndex_list)
    for key, value in combined_wordFrequency_dict.items():
        docCount_includeKey = 0
        for TF_ofWord in value: #value = List
            if (TF_ofWord != 0):
                docCount_includeKey += 1
        
        #IDF = log(총 문서 수 / 해당 단어를 가지고 있는 문서 수)
        idf_ofKey = log10(documentCount/docCount_includeKey)

        for valueIndex in range(0, len(validIndex_list)):
            combined_wordFrequency_dict[key][valueIndex] *= idf_ofKey   #IDF 곱함

    
    #5. targetURL에 대한 TF-IDF[word, TF-IDF] 값만 뽑아내고 리스트로 만들어 정렬
    tfidf_list = list()

    for key in combined_wordFrequency_dict.keys():
        elementList = list()
        elementList.append(key)  #word
        elementList.append(combined_wordFrequency_dict[key][targetURL_index])
        tfidf_list.append(elementList)

    tfidf_list.sort(reverse=True, key = lambda li:li[1])  #TF-IDF값 기준으로 내림차순 정렬

    return tfidf_list
        




            


