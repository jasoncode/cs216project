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
        data = requests.get('https://api.nytimes.com/svc/archive/v1/2016/1.json?api-key=64c18adc14cb43049ea3e5e74bdc7a49').json()
        return data
                
    except URLError, e:
        print 'Got an error code:', e
    
def findURLs(control, response, numArticles):
    if 0 in control:
        with open('response.txt', 'w') as outfile:
            json.dump(response, outfile)
    
    if 1 in control:
        counter = 0
        urls = []
        for i in range(response["response"]["meta"]["hits"]):
            article = response["response"]["docs"][i]
            if article["type_of_material"] == "News" and article["news_desk"] == "National":
                urls.append(article["web_url"])
                counter += 1
            if counter >= numArticles:
                break
        
        writeURLs('NYTUrls.txt', urls)
            
    if 2 in control:
        counter = 0
        urls = []
        for i in range(response["response"]["meta"]["hits"]):
            article = response["response"]["docs"][i]
            if article["type_of_material"] == "Blog":
                urls.append(article["web_url"])
                counter += 1
            if counter >= numArticles:
                break
        
        writeURLs('NYTBlogUrls.txt', urls)
    return

def writeURLs(filename, urls):
    with open(filename, 'w') as outfile:
        for item in urls:
            outfile.write(item + '\n')
    return
    
if __name__ == "__main__":
    response = getAPIReponse()
    
    #There's probly a more elegant way to do this, but basically this just passes a list of integers into the findURLs method,
    #and those integers control what data is written to files
    control = [0, 1, 2]
    findURLs(control, response, 20)
    

    