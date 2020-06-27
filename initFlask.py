#!/usr/bin/python
from flask import Flask
from flask import render_template
from flask import request
from elasticsearch import Elasticsearch
from Single_website_Crawler import URLData, analyze_URL_words, jsonify_URLData
from time import sleep
import pdb

app = Flask(__name__)
app.config['DEBUG'] = True

#Program 전반에 사용되는 elasticSearch Object
elasticStream = Elasticsearch()



@app.route('/')
def startPage():
    return render_template('index.html')  # Initial 웹사이트


@app.route('/singleURL', methods=['POST'])
def singleURL_processing_page():
    if (request.method == 'POST'):
        requestedURL = request.form['url'] #get singleURL from input Box
        URL_res = URLData()

    
        try:
            #(엘라스틱 서치 no설치환경에서 실행시 이거 주석처리)
            #isExist : 이미 ElasticSearch에 존재하는 URL이면 1 아니면 0을 반환합니다. 조금 더 상세한 로직은 elastic_test.py 2 참고
            isExist = elasticStream.search(body={"query":{"match":{"URL.keyword":requestedURL}}}, index='urldata', doc_type='website')['hits']['total']['value']
            if isExist != 0:
                raise Exception("Already Exist URL")
            ######

            URL_res = analyze_URL_words(requestedURL)
        except Exception as e: #URL 요청 실패
            print(e)
            # pdb.set_trace()
            return render_template('index.html', wordDictionary={}, succeed=False, isRootPage=True)

    # pdb.set_trace()
    return render_template('index.html', wordDictionary=jsonify_URLData(URL_res), succeed=True, isRootPage=False)


if __name__=='__main__':
    ipAddress='127.0.0.1'
    print("Starting the service with ipAddress = " + ipAddress)
    listen_port = 5555


    #insert to ElasticSearch(엘라스틱 서치 no설치환경에서 실행시 이거 주석처리)
    try:
        elasticStream = Elasticsearch([{'es_host':ipAddress, 'es_port':'9200'}], timeout=30)
        print("Open elasticSearch!\n")
    except Exception as e:
        print(e)
        print("elastic Stream Error \n")
    ####


    app.run(debug=True, host = ipAddress, port=int(listen_port))


    