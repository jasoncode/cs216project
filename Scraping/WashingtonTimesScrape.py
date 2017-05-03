from lxml import html
import sys
import scrapingutil as scrape

def getUrls(numUrls):
    urls = []
    base_path = 'http://www.washingtontimes.com/'
    page_num = 1
    while len(urls) < numUrls:
        tree = scrape.getHTML('http://www.washingtontimes.com/news/politics/?page=' + str(page_num))
        extensions =  tree.xpath('//section[@class="block article-list related-articles"]/article/h2/a/@href')
        if page_num == 1:
            extensions.extend(tree.xpath('//div[@class="block article-list featured-articles"]/article/h2/a/@href'))
        print extensions
        if extensions == []:
            break
        urls.extend([base_path + extension for extension in extensions])
        page_num += 1
    
    return urls[0:numUrls]
            
def scraper(url):
    tree = scrape.getHTML(url) 
    paragraphs = tree.xpath('//div[@class="storyareawrapper"]/div[@class="bigtext"]/p') 
    paragraphsUTF = []
    
    for paragraph in paragraphs:
        paragraphsUTF.append(scrape.encodeParagraph(paragraph.text_content()))    
    
    return paragraphsUTF

if __name__ == "__main__":
    urls = getUrls(500)
    scrape.writeArticleFile('./RealNews/WashingtonTimesArticles', urls, sys.modules[__name__])
   
    
    
    