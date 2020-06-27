#!/usr/bin/python
from elasticsearch import Elasticsearch



elasticStream = Elasticsearch()




if __name__=="__main__":
    ipAddress='127.0.0.1'
    elasticStream = Elasticsearch([{'es_host':ipAddress, 'es_port':'9200'}], timeout=30)

    import Multi_website_Crawler
    URL_list = Multi_website_Crawler.multi_URL_analyze("URL_test.txt")

    print(len(URL_list))

    for dic in URL_list:
        print(dic, '\n\n')

    



def webSiteCount():
    # 1. 현재 elastic에 저장된 웹페이지 개수를 반환함. (int)
    elasticWebsiteCount = elasticStream.count(index='urldata', doc_type='website')['count']
    print(elasticWebsiteCount)


    

def matching():
    nowWeb='https://apache.org/'
    # 2. URL match(정확히 일치) 검색. (dictonary return)
    doc = elasticStream.search(body={"query":{"match":{"URL.keyword":nowWeb}}}, index='urldata', doc_type='website')['hits']['total']['value']

    
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

    