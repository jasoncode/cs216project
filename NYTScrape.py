import json
from lxml import html
import requests

def setup():
    with open('NYTUrls.txt') as infile:    
        urls = infile.readlines()

    with open('NYTArticles.txt', 'w') as outfile:
        for url in urls:
            outfile.write('ARTICLE\n')
            paragraphs = parser(url)
            for text in paragraphs:
                outfile.write(text + '\n')
            outfile.write('\n\n\n')
            
def parser(url):
    data = requests.get(url)
    tree = html.fromstring(data.content)
    
    paragraphs = tree.xpath('//article/div[@class="story-body-supplemental"]/div/p[@class="story-body-text story-content"]')
    paragraphsUTF = []
    
    for paragraph in paragraphs:
        paragraph = paragraph.text_content().encode('latin1')
        paragraphsUTF.append(paragraph)   
    
    return paragraphsUTF
    
setup()