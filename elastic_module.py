from elasticsearch import Elasticsearch, NotFoundError
from time import sleep

#Program 전반에 사용되는 elasticSearch Object
elasticStream = Elasticsearch()


#launch elasticSearch
def launch_elasticSearch():

    #elasticSearch Object를 생성하고, 연결합니다.
    try:
        elasticStream = Elasticsearch([{'es_host':'127.0.0.1', 'es_port':'9200'}], timeout=30)
        print("Open elasticSearch!\n")
    except Exception as e:
        print(e)
        print("elastic Stream Error \n")
    

    #elasticSearch가 완전히 연결될때까지 대기합니다. 
    # (25초가 넘어가면 문제가 생긴 것으로 판단하고 실패처리 합니다.)
    for waitTime in range(0, 30):
        try:
            print('waiting for Elasticsearch Connection : Time = ', waitTime)
            sleep(1)
            #It's Not Error
            elasticStream.cluster.health(wait_for_status='yellow')
            break
        except Exception as e:
            if waitTime >= 25:
                print("elasticSearch seems Connection Problem")
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
    