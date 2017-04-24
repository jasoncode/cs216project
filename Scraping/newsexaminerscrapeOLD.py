from lxml import html
import requests

def getUrls():
    data = requests.get('http://www.newsexaminer.com/news/election_politics/')
    tree = html.fromstring(data.content)
    
    urls = tree.xpath('//div[@id="tncms-region-index-primary"]//div[@class="card-headline"]//a/@href')
    return urls

def getArticles(urls):
    with open('NewsExaminerArticles.txt', 'w') as outfile:
        for url in urls:
            outfile.write('ARTICLE\n')
            paragraphs = scraper(url)
            for text in paragraphs:
                outfile.write(text + '\n')
            outfile.write('\n\n\n')
            
def scraper(url):
    data = requests.get('http://www.newsexaminer.com' + url)
    tree = html.fromstring(data.content)
    paragraphsUTF = []
    
    paragraphs = tree.xpath('//div[@class="asset-content  subscriber-premium"]//p')   
    
    for paragraph in paragraphs:
        paragraph = paragraph.text_content().encode('latin1').decode('utf-8').encode('utf-8')
        
        #extra content at the end of some articles
        if paragraph == '---' or 3*paragraph.count('\xe2') == len(paragraph):
            break
        paragraphsUTF.append(paragraph)   
    
    return paragraphsUTF

if __name__ == "__main__":
    urls = getUrls()
    getArticles(urls)
   
    
    
    