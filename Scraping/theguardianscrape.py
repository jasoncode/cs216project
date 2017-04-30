from lxml import html
import sys
import scrapingutil as scrape

def getUrls(numUrls):
    urls = []

    counter = 0
    while len(urls) < numUrls:
        tree = scrape.getHTML('https://www.theguardian.com/us-news/us-politics?page=' + str(counter))   
        newUrls = tree.xpath('//div[@class="u-cf index-page"]/section//a/@href')
        for url in newUrls:
            if '/us-news/2017/' in url:
                urls.append(url)
        counter += 1
        urls = list(set(urls))
    
    return urls[0:numUrls]
            
def scraper(url):
    tree = scrape.getHTML(url) 
    paragraphs = tree.xpath('//div[@class="content__article-body from-content-api js-article__body"]/p') 
    paragraphsUTF = []
    
    for paragraph in paragraphs:
        paragraphsUTF.append(scrape.encodeParagraph(paragraph.text_content()))    
    
    return paragraphsUTF

if __name__ == "__main__":
    urls = getUrls(500)
    print 'LENGTH', len(urls)
    scrape.writeArticleFile('./RealNews/TheGuardianArticles', urls, sys.modules[__name__])
   
    
    
    