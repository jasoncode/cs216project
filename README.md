Group 6 Midterm Report
CS 216

Github link: https://github.com/jasoncode/cs216project

# Summary

So far, we have scraped articles from the New York Times, and ran successful tests using one of the sentiment analysis Python libraries we plan on using. For more info, see the specific sections of this report. Our main challenges going forward will be scraping the fake news sites that are often cluttered and poorly coded, and choosing the smartest and most telling visualizations for our data. In order to best narrow down our field of interest, we will only consider political news articles. It was the 2016 election that brought fake news into the spotlight, so analyzing politically charged articles will provide us with the most interesting and relevant results.

Complications so far have been in defining and identifying fake news. Some sites intentionally mix real and fake news, which affects our ability to delimit the sites. Also, many sites include a disclaimer that nothing they write should be trusted. If a site gives up its hoax, is it still fake news,or satire? These questions have led us to reconsider how we will visualize our data, because it may not be wise to clump all fake sites into one category. Therefore, we are attempting to analyze only those news sites that claim legitimacy, though this is proving to be a challenge. 

#### ‘Fake’ Sources:  
http://libertywriters.com  
http://yournewswire.com/category/news/us/  
http://countercurrentnews.com/  
http://www.naturalnews.com   
http://rilenews.com  
http://politicops.com/politics/  

#### Real News Sites & APIS  
Associated Press: https://www.programmableweb.com/api/associated-press-breaking-news  
Economist (www.economist.com) (see www.newsapi.org)  
Wall Street Journal (www.wsj.com) (see www.newsapi.org)  
National Review (www.nationalreview.com) (see www.newsapi.org)  
Fox News (www.foxnews.com) (see http://www.foxnews.com/story/2007/11/09/foxnewscom-rss-feeds.html)  
http://www.newsexaminer.com   (http://www.newsexaminer.com/news/election_politics/)  
NYT  
The Guardian  

# Data Collection:

We will use python to acquire data from news sources. The first step to acquiring news articles is getting a list of URLs to articles we want to use. For some sources this will be possible through an API call, such as the New York Times. For others we will need to scrape these URLs from the website itself. Once we have URLs to a sufficient number of articles, we will scrape the article text from the website. We are using the python library lxml, in combination with xpath, in order to scrape data. These tools allow us to easily access specific sections of the html and acquire all text from that section and child sections. For example, many articles are constructed with sequential <p> tags, often with child tags for things like links. Lxml and xpath allow us to acquire all of the text in just a few lines. We then encode the text to normalize format, and write it to a text file (for now, may use different storage later). This text file is then used as input for the sentiment analysis. 
We have gone through the entire process with the New York Times, and it has worked quite well. The main data collection work moving forwards will be scraping the rest of the websites listed in the sources section. Currently the text files on the github are just for testing purposes, as mentioned earlier we will focus on politics for the remainder of our project.

# Methodology: Sentiment Analysis:

We have downloaded a Python library called textblob which enables sentiment analysis based on its extensive corpora. The documentation for the library is at the following link for additional information on the library as a whole: https://textblob.readthedocs.io/en/dev/. The key aspect for our project is the sentiment feature, which returns a two-element tuple consisting of polarity, on a scale of -1 for most negative to 1 for most positive, and subjectivity, on a scale of 0 for most objective to 1 for most subjective. The file textblob_test.py includes several intuitive example sentences demonstrating the functionality. 
The test file also demonstrates the use of textblob on the New York Times articles collected (as described above). It outputs a clear heading for each type of source (articles and blogs) , labels for subjectivity and polarity, and a 2-value row for each article with those two values as a .csv file (currently called results.csv). Both textblob_test.py and results.csv are in the sentiment_analysis_testing folder of the Github. Once we have collected data from all of the various sources listed above, we will be able to compute various features of each news source, including distributions, means, and medians of these two sentiment metrics. 
Furthermore, textblob may not be the only source of sentiment analysis we use. There are several Python libraries that conduct sentiment analysis, and we may choose to compare or even average the results of several of these libraries to achieve the most comprehensive result.

# Analysis and Visualization:

Once we have our two-dimensional (polarity and subjectivity) data for all of our articles, we will have many different options to conduct insightful analysis. Since we only have data from the New York Times so far, we have created scatter plots demonstrating the type of visualizations we may perform. These plots place subjectivity on the x-axis and polarity on the y-axis, creating a clear (if small) picture of the sentiment analysis of the New York Times articles we pulled. This also provides a path forward for our first steps of data visualization: averaging the polarity and sentiment for each news source will allow us to plot them on this 2-D graph and hopefully identify basic trends in real news vs. fake news and news from the left or right of the aisle. Plotting the data in this way will also guide our analysis and visualization going forward.
