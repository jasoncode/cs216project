from lxml import html
import sys
import scrapingutil as scrape

def getUrls():
    urls = []
    #number of pages, there are 15 articles per page
    for i in range(1, 9):
        tree = scrape.getHTML('http://countercurrentnews.com/category/corruption/page/' + str(i) + '/')   
        urls.extend(tree.xpath('//article/div[@class="post-thumb"]/a/@href'))
    
    return urls
            
def scraper(url):
    tree = scrape.getHTML(url) 
    paragraphs = tree.xpath('//article/div[@class="entry-content"]/p[not(descendant::script)]|//article/div[@class="entry-content"]/blockquote/p') 
    paragraphsUTF = []
    
    for paragraph in paragraphs:
        paragraph = scrape.encodeParagraph(paragraph.text_content())
        if paragraph.startswith(("(Article by", "(Article By", "(Article From", "(from", "Article by")):
            break
            
        paragraphsUTF.append(paragraph)
    
    return paragraphsUTF

if __name__ == "__main__":
    urls = getUrls()
    scrape.writeArticleFile('./FakeNews/CounterCurrentNewsArticles', urls, sys.modules[__name__])
   
    
    
    