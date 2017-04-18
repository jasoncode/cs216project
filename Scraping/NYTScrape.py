import json
from lxml import html
import requests

def getArticles(filename):
    with open(filename) as infile:    
        urls = infile.readlines()

    prefix = filename.split('.')[0].replace("Urls", "")
    
    with open(prefix + 'Articles.txt', 'w') as outfile:
        for url in urls:
            outfile.write('ARTICLE\n')
            paragraphs = scraper(url, prefix)
            for text in paragraphs:
                outfile.write(text + '\n')
            outfile.write('\n\n\n')
            
def scraper(url, prefix):
    data = requests.get(url)
    tree = html.fromstring(data.content)
    paragraphsUTF = []
    
    if prefix in ['NYTNational', 'NYTPolitical']:
        paragraphs = tree.xpath('//article/div[@class="story-body-supplemental"]/div/p[@class="story-body-text story-content"]')
    elif prefix == 'NYTBlog':
        paragraphs = tree.xpath('//article/div[@class="entry-content"]/p')
    
    
    for paragraph in paragraphs:
        if prefix in ['NYTNational', 'NYTPolitical']:
            paragraph = paragraph.text_content().encode('latin1').decode('utf-8').encode('utf-8')
        elif prefix == 'NYTBlog':
            paragraph = paragraph.text_content().encode('utf-8')
        paragraphsUTF.append(paragraph)   
    
    return paragraphsUTF

if __name__ == "__main__":
    getArticles('NYTNationalUrls.txt')
    getArticles('NYTBlogUrls.txt')
    getArticles('NYTPoliticalUrls.txt')       
    
    
    