from elasticsearch import Elasticsearch, NotFoundError
from time import sleep

#Program 전반에 사용되는 elasticSearch Object
elasticStream = Elasticsearch()


#launch elasticSearch
def launch_elasticSearch():

    #elasticSearch Object를 생성하고, 연결합니다.
    try:
        elasticStream = Elasticsearch([{'es_host':'127.0.0.1', 'es_port':'9200'}], timeout=100)
        print("Open elasticSearch!\n")
    except Exception as e:
        print(e)
        print("elastic Stream Error \n")
    

    #elasticSearch가 완전히 연결될때까지 대기합니다. 
    # (25초가 넘어가면 문제가 생긴 것으로 판단하고 실패처리 합니다.)s
    for waitTime in range(0, 100):
        try:
            print('waiting for Elasticsearch Connection : Time = ', waitTime)
            sleep(1)
            #It's Not Error
            elasticStream.cluster.health(wait_for_status='yellow')
            break
        except Exception as e:
            if (waitTime >= 90):
                print("It tooks Too much time to connect.")
                return


    #elasticSearch index에서 받을 수 있는 데이터 상한을 20배 늘립니다.
    elasticSettings = { 
        'settings': {
            'index.mapping.total_fields.limit':20000
        }
    }


    #website Index가 생성된 바가 없는 경우에만 위 상한 확장을 진행합니다.
    try:
        elasticStream.search(index='website')
    except NotFoundError:
        elasticStream.indices.create(index='website', body=elasticSettings)

    print('elasticSearch setting Complete')





#ElasticSearch에서, _id 번호에 websiteData(jsonified)를 삽입합니다.  (no return)
def insert_elasticSearch(websiteData, _id):
    print("Add urlData to ElasticSearch id = ", _id, ". URL = ", websiteData['URL'])

    saveData = elasticStream.index(index='website', doc_type='urldata', id=_id, body=websiteData)
    if saveData == False:
        print("\nURLData Saving to Elastic Failed..\n")
    


#ElasticSearch에서, 인자로 전해준 URL에 대한 Dictionary가 이미 존재하는 지 검색합니다.
#반환은 boolean 타입.
def search_urlMatch(URL):
    searchHits = elasticStream.search(body={"query":{"match":{"URL.keyword":URL}}},\
            index='website', doc_type='urldata')['hits']['total']['value']
    
    if searchHits >= 1:
        return True
    else:
        return False


#website index가 존재하는 경우, index 내부 값을 싹 비워버리고 새로 생성합니다. (no return)
#실행되지도 않은 elasticSearch에 대한 예외는 보증하지 않습니다.
def clear_elasticSearch_data():
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
    
