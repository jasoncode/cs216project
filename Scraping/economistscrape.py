from lxml import html
import sys
import scrapingutil as scrape

def getUrls(numUrls):
    urls = []
    base_path = 'http://www.economist.com/'
    page_num = 1
    while len(urls) < numUrls:
        tree = scrape.getHTML('http://www.economist.com/sections/united-states?page=' + str(page_num))
        extensions =  tree.xpath('//div[@class="teaser-list"]/article/a/@href')
        if extensions == []:
            break
        urls.extend([base_path + extension for extension in extensions])
        page_num += 1
    
    return urls[0:numUrls]
            
def scraper(url):
    tree = scrape.getHTML(url) 
    paragraphs = tree.xpath('//div[@class="blog-post__text"]/p') 
    paragraphsUTF = []
    
    for paragraph in paragraphs:
        paragraphsUTF.append(scrape.encodeParagraph(paragraph.text_content()))    
    
    return paragraphsUTF

if __name__ == "__main__":
    urls = getUrls(500)
    scrape.writeArticleFile('./RealNews/TheEconomistArticles', urls, sys.modules[__name__])
   
    
    
    