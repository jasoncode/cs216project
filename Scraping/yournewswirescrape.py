from lxml import html
import sys
import scrapingutil as scrape

def getUrls():
    urls = []
    #number of pages, there 10 articles per page
    for i in range(1, 50):
        tree = scrape.getHTML('http://yournewswire.com/category/news/us/page/' + str(i) + '/')   
        urls.extend(tree.xpath('//article/div/header/h3/a/@href'))
    
    return urls
            
def scraper(url):
    tree = scrape.getHTML(url) 
    paragraphs = tree.xpath('//article/div[@class="entry-content clearfix"]/p') 
    paragraphsUTF = []
    
    for paragraph in paragraphs:
        paragraphsUTF.append(scrape.encodeParagraph(paragraph.text_content()))    
    
    return paragraphsUTF

if __name__ == "__main__":
    urls = getUrls()
    scrape.writeArticleFile('./FakeNews/YourNewsWireArticles', urls, sys.modules[__name__])
   
    
    
    