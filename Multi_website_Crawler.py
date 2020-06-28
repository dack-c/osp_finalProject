from Single_website_Crawler import URLData, analyze_URL_words, jsonify_URLData
import elastic_module


#Input : URL이 한 줄씩 적혀있는 리스트.
#Output : wordDictonary를 순서대로 모아둔 List
def multi_URL_analyze(f):
    #f = open(filename, "r")
    
    textLine = 0
    wordDictionaryList = []

    while True:
        URL_line = f.readline()
        if URL_line == '': #End of File
            break
        
        #URL 문자열 끝의 개행문자를 없앱니다.
        URL_line = URL_line.strip()

        textLine += 1
        
        
        URL_res = analyze_URL_words(URL_line)
        #analyze 메소드 내에서, URL 중복 및 유효성 검사를 실시합니다.

        elastic_module.insert_elasticSearch(URL_res, textLine)
        wordDictionaryList.append(URL_res)


        #정상 상태 URL이 아닐때, 콘솔에 해당 사항을 출력합니다.
        dictonary_status = URL_res['url_status']
        if (dictonary_status != 0):
            if (dictonary_status == 1):
                print('Invalid URL', end=' ')
            elif (dictonary_status == 2):
                print('Duplicated URL', end=' ')

            print('at URL_text file in Line ', textLine)




    f.close()

    return wordDictionaryList