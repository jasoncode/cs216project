from lxml import html
import sys
import scrapingutil as scrape

def getUrls(numUrls):
    urls = []
    page_num = 2
    while len(urls) < numUrls:
        tree = scrape.getHTML('http://www.oann.com/category/politics/page/' + str(page_num))
        extensions =  tree.xpath('//div[@id="main-content"]/article/header/h3/a/@href')
        urls.extend(extensions)
        page_num += 1
        if len(urls) % 99 == 0:
            print len(urls)
    return urls[0:numUrls]
            
def scraper(url):
    tree = scrape.getHTML(url) 
    paragraphs = tree.xpath('//div[@class="entry-content clearfix"]/p') 
    paragraphsUTF = []
    
    for paragraph in paragraphs:
        encoded_par = scrape.encodeParagraph(paragraph.text_content()).strip()
        if not encoded_par.startswith('('):
            paragraphsUTF.append(encoded_par)    
    
    return paragraphsUTF

if __name__ == "__main__":
    urls = getUrls(500)
    scrape.writeArticleFile('./RealNews/OANNArticles', urls, sys.modules[__name__])
   
    
    
    