#!/usr/bin/python
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import elastic_module
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

    
        try:
            URL_res = analyze_URL_words(requestedURL)
            elastic_module.insert_elasticSearch(URL_res, 1)
        except Exception as e: #URL 요청 실패
            print(e)
            # pdb.set_trace()
            # return render_template('index.html', wordDictionary={}, succeed=False, isRootPage=True)
            #html 파일 수정되면... 위 라인을 아랫줄 구문으로 바꾸시오
            return render_template('index.html', wordDictionary={}, succeed=False, pageStatus=1)


    # pdb.set_trace()
    # return render_template('index.html', wordDictionary=URL_res, succeed=True, isRootPage=False)
    #html 파일 수정되면... 위 라인을 아랫줄 구문으로 바꾸시오
    return render_template('index.html', wordDictionary=URL_res, succeed=True, pageStatus=1)



@app.route('/multiURL', methods=['POST'])
def multiURL_processing_page():
    if (request.method == 'POST'):
        URL_textFile = request.files['txt']
        URL_textFile.save(secure_filename(URL_textFile.filename))

        #다중 웹사이트 분석 결과를 리스트 형태로 받아옵니다.
        URL_analyzeList = multi_URL_analyze(URL_textFile.filename)
        
        #유효한 URL이 하나도 없다면 실패 반환
        if (len(URL_analyzeList) == 0):
            return render_template('index.html', wordDictionaryList=[], succeed=False, pageStatus=2)  #매개변수들 주의
    
    return render_template('index.html', wordDictionaryList=URL_analyzeList, succeed=True, pageStatus=2)  #매개변수들 주의

if __name__=='__main__':
    ipAddress='127.0.0.1'
    print("Starting the service with ipAddress = " + ipAddress)
    listen_port = 5555

    #launch ElasticSearch
    elastic_module.launch_elasticSearch()

    app.run(debug=True, host = ipAddress, port=int(listen_port), use_reloader=False)


    