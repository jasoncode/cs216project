from lxml import html
import sys
import scrapingutil as scrape

def getUrls():
    urls = []
    #number of pages, there 10 articles per page
    for i in range(1, 50):
        tree = scrape.getHTML('http://www.reuters.com/news/archive/politicsNews?view=page&page=' + str(i) + '&pageSize=10' )   
        urls.extend(tree.xpath('//div[@class="news-headline-list medium"]/article/div[@class="story-content"]/a/@href'))
    
    return urls
            
def scraper(url):
    tree = scrape.getHTML('http://www.reuters.com' + url) 
    paragraphs = tree.xpath('//span[@id="article-text"]//p')[0:-1]
    paragraphsUTF = []
    
    for paragraph in paragraphs:
        paragraphsUTF.append(scrape.encodeParagraph(paragraph.text_content()))    
    
    return paragraphsUTF

if __name__ == "__main__":
    urls = getUrls()
    scrape.writeArticleFile('./RealNews/ReutersArticles', urls, sys.modules[__name__])
   
    
    
    