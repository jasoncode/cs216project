from lxml import html
import sys
import scrapingutil as scrape

def getUrls():
    urls = []
    #number of pages
    for i in range(2, 35):
        tree = scrape.getHTML('https://www.theatlantic.com/politics/?page=' + str(i))   
        urls.extend(tree.xpath('//div[@class="river-body"]/ul[@class="river"]/li[@class="article blog-article "]/a/@href'))
    
    urls = [x for x in urls if 'politics/archive/' in x]
    return urls[0:500]
            
def scraper(url):
    tree = scrape.getHTML('https://www.theatlantic.com/' + url) 
    paragraphs = tree.xpath('//div[@class="article-body"]/section/p|//div[@class="article-body"]/section/blockquote') 
    paragraphsUTF = []
    
    for paragraph in paragraphs:
        paragraphsUTF.append(scrape.encodeParagraph(paragraph.text_content()))    
    
    return paragraphsUTF

if __name__ == "__main__":
    urls = getUrls()
    print len(urls), len(set(urls))
    scrape.writeArticleFile('./RealNews/TheAtlanticArticles', urls, sys.modules[__name__])
   
    
    
    