from urllib2 import Request, urlopen, URLError
import requests
import json

#request = Request('https://newsapi.org/v1/sources')
#request = Request('https://newsapi.org/v1/articles?source=bbc-news&sortBy=latest&apiKey=bf6dc10268614c818ab068c14edf9707')
#request = Request('https://newsapi.org/v1/articles?source=the-next-web&sortBy=latest&apiKey=bf6dc10268614c818ab068c14edf9707')

def getAPIReponse():
    try:
        #response = urlopen(request)
        #resp = response.read()
        #json = json.load(resp)
        #data = requests.get('https://newsapi.org/v1/articles?source=the-next-web&sortBy=latest&apiKey=bf6dc10268614c818ab068c14edf9707').json()
        #data = requests.get('https://api.nytimes.com/svc/search/v2/articlesearch.json?api-key=64c18adc14cb43049ea3e5e74bdc7a49').json()
        
        #Jan 2016
        #data = requests.get('https://api.nytimes.com/svc/archive/v1/2016/1.json?api-key=64c18adc14cb43049ea3e5e74bdc7a49').json()
        
        #March 2017
        data1 = requests.get('https://api.nytimes.com/svc/archive/v1/2016/10.json?api-key=64c18adc14cb43049ea3e5e74bdc7a49').json()
        data2 = requests.get('https://api.nytimes.com/svc/archive/v1/2016/11.json?api-key=64c18adc14cb43049ea3e5e74bdc7a49').json()
        return data2, data1
                
    except URLError, e:
        print 'Got an error code:', e
    
def findURLs(control, response, numArticles):
    if 0 in control:
        with open('NYTResponse.txt', 'w') as outfile:
            json.dump(response, outfile)
    
    #gets national news articles
    if 1 in control:
        counter = 0
        urls = []
        for i in range(0, response["response"]["meta"]["hits"]-1):
            article = response["response"]["docs"][i]
            if article["type_of_material"] == "News" and article["news_desk"] == "National":
                urls.append(article["web_url"])
                counter += 1
            if counter >= numArticles:
                break
        
        writeURLs('NYTNationalUrls.txt', urls)
    
    #gets blog articles    
    if 2 in control:
        counter = 0
        urls = []
        for i in range(0, response["response"]["meta"]["hits"]-1):
            article = response["response"]["docs"][i]
            if article["type_of_material"] == "Blog":
                urls.append(article["web_url"])
                counter += 1
            if counter >= numArticles:
                break
        
        writeURLs('NYTBlogUrls.txt', urls)
    
    #gets political articles
    if 3 in control:
        counter = 0
        urls = []
        for i in range(0, response["response"]["meta"]["hits"]-1):
            article = response["response"]["docs"][i]
            if article["type_of_material"] == "News" and article["news_desk"] == "National" and 'us/politics' in article["web_url"]:
                urls.append(article["web_url"])
                counter += 1
            if counter >= numArticles:
                break
        return urls
            
    return

def writeURLs(filename, urls):
    with open(filename, 'w') as outfile:
        for item in urls:
            outfile.write(item + '\n')
    return
    
if __name__ == "__main__":
    response = getAPIReponse()
    numUrls = 500
    
    #There's probly a more elegant way to do this, but basically this just passes a list of integers into the findURLs method,
    #and those integers control what data is written to files
    #0 dump nyt response to file
    #1 get national news article urls
    #2 get blog article urls
    #3 get political article urls
    control = [3]
    urls2 = findURLs(control, response[0], numUrls)
    if len(urls2) < numUrls:
        urls1 = findURLs(control, response[1], numUrls-len(urls2))
    urls2.extend(urls1)
    writeURLs('NYTPoliticalUrls.txt', urls2) 
    