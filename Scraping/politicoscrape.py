from lxml import html
import sys
import scrapingutil as scrape

def getUrls():
    urls = []
    #number of pages, there 9 articles per page
    for i in range(1, 57):
        tree = scrape.getHTML('http://www.politico.com/white-house/' + str(i))   
        urls.extend(tree.xpath('//div[@class="content-group tag-latest"]/ul/li/article/figure/div/a/@href'))
    
    return urls[0:500]
            
def scraper(url):
    tree = scrape.getHTML(url) 
    paragraphs = tree.xpath('//div[@class="story-text "]/p') 
    paragraphsUTF = []
    
    for paragraph in paragraphs:
        paragraphsUTF.append(scrape.encodeParagraph(paragraph.text_content()))    
    
    return paragraphsUTF

if __name__ == "__main__":
    urls = getUrls()
    print len(urls), len(set(urls))
    scrape.writeArticleFile('./RealNews/PoliticoArticles', urls, sys.modules[__name__])
   
    
    
    