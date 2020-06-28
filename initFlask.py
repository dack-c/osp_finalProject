#!/usr/bin/python
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import elastic_module
import dataAnalysis_module
from Single_website_Crawler import URLData, analyze_URL_words, jsonify_URLData
from Multi_website_Crawler import multi_URL_analyze

import pdb

app = Flask(__name__)
app.config['DEBUG'] = True



@app.route('/')
def startPage():
    return render_template('index.html')  # Initial 웹사이트


@app.route('/singleURL', methods=['POST'])
def singleURL_processing_page():
    if (request.method == 'POST'):
        requestedURL = request.form['url'] #get singleURL from input Box
        URL_res = URLData()

        
        elastic_module.clear_elasticSearch_data()  #데이터 초기화
        URL_res = analyze_URL_words(requestedURL)
        elastic_module.insert_elasticSearch(URL_res, 1)
        
        
        if (URL_res['url_status'] == 0):    #반환받은 Dictionary의 상태가 정상이면 succeed=True
            return render_template('index.html', wordDictionary=URL_res, succeed=True, pageStatus=1)
        else:
            return render_template('index.html', wordDictionary=URL_res, succeed=False, pageStatus=1)


    



@app.route('/multiURL', methods=['POST'])
def multiURL_processing_page():
    if (request.method == 'POST'):
        URL_textFile = request.files['txt']
        URL_textFile.save(secure_filename(URL_textFile.filename))

        elastic_module.clear_elasticSearch_data()
        
        #다중 웹사이트 분석 결과를 리스트 형태로 받아옵니다.
        global URL_analyzeList
        URL_analyzeList = multi_URL_analyze(URL_textFile.filename)
        
        #유효한 URL이 하나도 없다면 실패 반환
        if (len(URL_analyzeList) == 0):
            return render_template('index.html', wordDictionaryList=[], succeed=False, pageStatus=2) 
    
    return render_template('index.html', wordDictionaryList=URL_analyzeList, succeed=True, pageStatus=2)



@app.route('/similarity', methods=['POST'])
def analyzeSimilarity():
    if (request.method == 'POST'):
        requestedURL = request.form['targetUrl'] #분석 대상이 될 url을 받음
    
        return render_template('cosine-similarity.html', targetUrl=requestedURL, \
            similarityList=dataAnalysis_module.get_cosine_similarity_list(URL_analyzeList, requestedURL)) #데이터 보내기


@app.route('/tf-idf', methods=['POST'])
def analyzetfidf():
    if (request.method == 'POST'):
        requestedURL = request.form['targetUrl'] #분석 대상이 될 url을 받음
    
        return render_template('tf-idf.html', targetUrl=requestedURL, \
            tfidfList=dataAnalysis_module.get_top_TFIDF_list(URL_analyzeList, requestedURL)) #데이터 보내기






if __name__=='__main__':
    ipAddress='127.0.0.1'
    print("Starting the service with ipAddress = " + ipAddress)
    listen_port = 5555

    #launch ElasticSearch
    elastic_module.launch_elasticSearch()

    app.run(debug=True, host = ipAddress, port=int(listen_port), use_reloader=False)


    