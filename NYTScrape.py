import json
from lxml import html
import requests

from pprint import pprint

def setup():
    with open('urls.txt') as infile:    
        urls = infile.readlines()

    with open('articleText.txt', 'w') as outfile:
        for url in urls:
            outfile.write('ARTICLE\n')
            paragraphs = parser(url)
            for text in paragraphs:
                outfile.write(text + '\n')
            outfile.write('\n\n\n')
            
def parser(url):
    data = requests.get(url)
    tree = html.fromstring(data.content)
    
    #currently this does not words that are also links, have to find a way to read <a> tag text in order somehow
    paragraphs = tree.xpath('//article/div[@class="story-body-supplemental"]/div/p[@class="story-body-text story-content"]/text()')
    paragraphsUTF = []
    
    #temporary hacky way to fix quotes, have to find better way to fix encoding problems since there
    #are a bunch more, just wanted to make sure it was possible
    weirdSingleQuote = paragraphs[3].encode('utf-8').strip()[12:18]
    weirdDoubleQuote = paragraphs[6].encode('utf-8').strip()[0:6]
    
    for paragraph in paragraphs:
        paragraphsUTF.append(paragraph.encode('utf-8').strip().replace(weirdSingleQuote, "\'").replace(weirdDoubleQuote, "\""))
        
    return paragraphsUTF
    
setup()