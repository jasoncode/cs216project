from lxml import html
import requests

"""
@param param1: url from which you want to get lxml formatted html content
"""
def getHTML(url):
    try:
        data = requests.get(url)
        tree = html.fromstring(data.content)
        return tree
        
    except Exception as e:
        print 'Got an error code:', e
        
"""
Basically this method takes a filename, a list of urls, and a module (which must contain a scraper function), and then
scrapes all of the articles from given urls and writes them to a text file for storage

@param param1: string of the name you want to use for the article text file
@param param2: list of urls for the articles
@param param3: module that is calling this method, look at a scrape file for an example of how to use this
@param param4: OPTIONAL param, if you pass a number here, only that article will be written to the file (this is for testing purposes)
"""       
def writeArticleFile(filename, urls, module, urlnum=None):
    with open(filename + '.txt', 'w') as outfile:
        if urlnum is None:
            for count, url in enumerate(urls):
                outfile.write('ARTICLE\n')
                paragraphs = module.scraper(url)
                for text in paragraphs:
                    outfile.write(text + '\n')
                outfile.write('\n\n\n')

                if count % 50 == 0:
                    print count
        else: 
            url = urls[urlnum]
            outfile.write('ARTICLE\n')
            paragraphs = module.scraper(url)
            for text in paragraphs:
                outfile.write(text + '\n')
            outfile.write('\n\n\n')  

def encodeParagraph(paragraph):
    try:
        paragraphUTF = paragraph.encode('utf-8')
        return paragraphUTF
    except Exception:
        pass
    try:
        paragraphUTF = paragraph.encode('latin1').decode('utf-8').encode('utf-8')
        return paragraphUTF
    except Exception as e:
        print 'Encoding failed:', e
    
    
    
    
    