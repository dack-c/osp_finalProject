from Single_website_Crawler import URLData, analyze_URL_words, jsonify_URLData
import elastic_module


#Input : URL이 한 줄씩 적혀있는 리스트.
#Output : wordDictonary를 순서대로 모아둔 List
def multi_URL_analyze(filename):
    f = open(filename, "r")
    
    websiteCount = 0
    textLine = 0
    wordDictionaryList = []

    while True:
        URL_line = f.readline()
        if URL_line == '': #End of File
            break
        
        #URL 문자열 끝의 개행문자를 없앱니다.
        URL_line = URL_line.strip()

        textLine += 1
        
        try:
            URL_res = analyze_URL_words(URL_line)
            #유효한 URL이 아니면 위 메소드에서 예외가 던져져서, 콘솔에 Error 출력하고
            #아래 try 블럭 내 작업은 수행되지 않습니다.
            websiteCount += 1
            elastic_module.insert_elasticSearch(URL_res, websiteCount)
            wordDictionaryList.append(URL_res)
        except Exception as e: #URL 요청 실패
            print('Exception at URL_text file in Line ', textLine)
            print(e)

    f.close()

    return wordDictionaryList