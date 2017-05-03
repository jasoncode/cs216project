from lxml import html
import sys
import scrapingutil as scrape

def getUrls(numUrls):
    urls = []
    base_path = 'http://www.nationalreview.com/'
    page_num = 0
    while len(urls) < numUrls:
        tree = scrape.getHTML('http://www.nationalreview.com/archives?page=' + str(page_num))
        extensions =  tree.xpath('//div[@class=" timeline blog cf p-r"]/ul//a/@href')
        if extensions == []:
            
            break
        urls.extend([base_path + extension for extension in extensions])
        page_num += 1
    
    return urls[0:numUrls]
            
def scraper(url):
    tree = scrape.getHTML(url) 
    paragraphs = tree.xpath('//div[@itemprop="articleBody"]/p') 
    paragraphsUTF = []
    
    for paragraph in paragraphs:
       stripped_par = scrape.encodeParagraph(paragraph.text_content()).strip()
       if len(stripped_par) > 0:
            paragraphsUTF.append(stripped_par)    
    
    return paragraphsUTF

if __name__ == "__main__":
    urls = getUrls(500)
    scrape.writeArticleFile('./RealNews/NationalReviewArticles', urls, sys.modules[__name__])
   
    
    
    