from lxml import html
import sys
import scrapingutil as scrape

def getUrls():
    urls = []
    #number of pages, there are 30 articles per page
    for i in range(1, 19):
        tree = scrape.getHTML('http://www.breitbart.com/big-government/page/' + str(i) + '/')   
        urls.extend(tree.xpath('//div[@class="article-list"]/article/a/@href'))
    return urls[0:500]
            
def scraper(url):
    tree = scrape.getHTML(url) 
    paragraphs = tree.xpath('//article/div[@class="entry-content"]/p|//article/div[@class="entry-content"]/blockquote') 
    paragraphsUTF = []
    
    for paragraph in paragraphs:
        paragraph = scrape.encodeParagraph(paragraph.text_content())
        paragraphsUTF.append(paragraph)
    
    return paragraphsUTF

if __name__ == "__main__":
    urls = getUrls()
    scrape.writeArticleFile('./RealNews/BreitbartArticles', urls, sys.modules[__name__])
   
    
    
    