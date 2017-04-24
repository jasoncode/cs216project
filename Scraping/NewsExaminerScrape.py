from lxml import html
import sys
import scrapingutil as scrape

def getUrls():
    tree = scrape.getHTML('http://www.newsexaminer.com/news/election_politics/')    
    urls = tree.xpath('//div[@id="tncms-region-index-primary"]//div[@class="card-headline"]//a/@href')
    return urls
            
def scraper(url):
    tree = scrape.getHTML('http://www.newsexaminer.com' + url) 
    paragraphs = tree.xpath('//div[@class="asset-content  subscriber-premium"]//p') 
    paragraphsUTF = []
    
    for paragraph in paragraphs:
        paragraph = paragraph.text_content().encode('latin1').decode('utf-8').encode('utf-8')
        
        #extra content at the end of some articles that we don't want
        if paragraph == '---' or 3*paragraph.count('\xe2') == len(paragraph):
            break
            
        paragraphsUTF.append(paragraph)   
    
    return paragraphsUTF

if __name__ == "__main__":
    urls = getUrls()
    scrape.writeArticleFile('NewsExaminerArticles', urls, sys.modules[__name__])
   
    
    
    