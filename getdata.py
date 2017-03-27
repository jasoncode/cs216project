from urllib2 import Request, urlopen, URLError
import requests
import json

#request = Request('https://newsapi.org/v1/sources')
#request = Request('https://newsapi.org/v1/articles?source=bbc-news&sortBy=latest&apiKey=bf6dc10268614c818ab068c14edf9707')
#request = Request('https://newsapi.org/v1/articles?source=the-next-web&sortBy=latest&apiKey=bf6dc10268614c818ab068c14edf9707')

try:
	#response = urlopen(request)
	#resp = response.read()
    #json = json.load(resp)
    #data = requests.get('https://newsapi.org/v1/articles?source=the-next-web&sortBy=latest&apiKey=bf6dc10268614c818ab068c14edf9707').json()
    #data = requests.get('https://api.nytimes.com/svc/search/v2/articlesearch.json?api-key=64c18adc14cb43049ea3e5e74bdc7a49').json()
    data = requests.get('https://api.nytimes.com/svc/archive/v1/2016/1.json?api-key=64c18adc14cb43049ea3e5e74bdc7a49').json()
    
    counter = 0
    urls = []
    for i in range(data["response"]["meta"]["hits"]):
        article = data["response"]["docs"][i]
        if article["type_of_material"] == "News" and article["news_desk"] == "National":
            urls.append(article["web_url"])
            counter += 1
        if counter >= 10:
            break
    
    '''with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)'''
        
    with open('urls.txt', 'w') as outfile:
        for item in urls:
            outfile.write(item + '\n')
            
except URLError, e:
    print 'Got an error code:', e