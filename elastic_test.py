#!/usr/bin/python
from elasticsearch import Elasticsearch, NotFoundError



elasticStream = Elasticsearch()




if __name__=="__main__":
    ipAddress='127.0.0.1'
    elasticStream = Elasticsearch([{'es_host':ipAddress, 'es_port':'9200'}], timeout=30)

    ###########################
    #Cosine Similiarity
    #input : DictonaryList와 비교 대상이 되는 Dictonary index(pivot) - pivot은 valid임이 보증됨
    #예를 들어 DictonaryList는 10의 길이를 지니고 DictonaryList[5]에 대한 코사인 유사도를 분석하는 것임
    #pivot = 1
    #wordDictonaryList_length = len()


    #

    elasticSettings = { 
        'settings': {
            'index.mapping.total_fields.limit':20000
        }
    }

    try:
        elasticStream.search(index='website')
        elasticStream.indices.delete(index='website')
    except NotFoundError:
        pass
        
    elasticStream.indices.create(index='website', body=elasticSettings)



    



def webSiteCount():
    # 1. 현재 elastic에 저장된 웹페이지 개수를 반환함. (int)
    elasticWebsiteCount = elasticStream.count(index='website', doc_type='urldata')['count']
    print(elasticWebsiteCount)


    

def matching():
    nowWeb='https://apache.org/'
    # 2. URL match(정확히 일치) 검색. (dictonary return)
    doc = elasticStream.search(body={"query":{"match":{"URL.keyword":nowWeb}}}, index='website', doc_type='urldata')['hits']['total']['value']

    
    #--> 존재하는 경우 반환값 예시
    #{
    # 'took': 1, 
    # 'timed_out': False, 
    # '_shards': {'total': 1, 'successful': 1, 'skipped': 0, 'failed': 0}, 
    # 'hits': {
    #   'total': {'value': 1, 'relation': 'eq'}, 
    #   'max_score': 0.2876821, 
    #   'hits': [
    #       {'_index': 'urldata', 
    #        '_type': 'website', 
    #        '_id': '1', 
    #        '_score': 0.2876821, 
    #        '_source': {
    #           'wordFrequency_dict': { (수많은 단어 분석 딕셔너리들) }, 
    #           'totalWord': 608, 
    #           'URL': 'https://apache.org/', 
    #           'caculateTime': 1.863595724105835, 
    #           'activated_on_site': True
    #         }
    #       }
    #   ]}}


    #--> 존재하지 않는 경우 반환값 예시
    #{
    # 'took': 1, 
    # 'timed_out': False, 
    # '_shards': {'total': 1, 'successful': 1, 'skipped': 0, 'failed': 0}, 
    # 'hits': {
    #   'total': {'value': 0, 'relation': 'eq'}, 
    #   'max_score': None, 
    #   'hits': [
    # ]}}


    #['hits']['total']['value'] == 0 이면 존재하지 않는 것, 1이면 존재하는 것이다.

    
    print('\n\n', doc)



def Multi_URL_simpleTester():
    #3. 멀티 웹사이트 크롤러 테스트
    import Multi_website_Crawler
    URL_list = Multi_website_Crawler.multi_URL_analyze("URL_test.txt")

    print("Total URLs = ", len(URL_list))
    for dic in URL_list:
        print(dic, '\n\n')