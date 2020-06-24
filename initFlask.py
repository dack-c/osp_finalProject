#!/usr/bin/python
from flask import Flask
from flask import render_template
from flask import request
from Single_website_Crawler import URLData, analyze_URL_words, jsonify_URLData
import pdb

app = Flask(__name__)


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
        except Exception as e: #URL 요청 실패
            print(e)
            pdb.set_trace()
            return render_template('index.html', wordDictionary={}, succeed=False)

    pdb.set_trace()
    return render_template('index.html', wordDictionary=jsonify_URLData(URL_res), succeed=True)


if __name__=='__main__':
    ipAddress="127.0.0.1"
    print("Starting the service with ipAddress = " + ipAddress)
    listen_port = 5555

    app.run(debug=True, host = ipAddress, port=int(listen_port))


    