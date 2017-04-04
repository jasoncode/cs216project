# -*- coding: utf-8 -*-

from textblob import TextBlob

def analyze_file(file_name):
	file = open(file_name,'r')
	sentences = []
	sentence = ""
	for line in file:
		utf_line = line.decode("utf-8")
		ascii_line  =utf_line.encode("ascii","ignore")
		if 'ARTICLE' in ascii_line:
			sentences.append(sentence)
			sentence = ""
		else:
			sentence+= " " + ascii_line
	for sentence in sentences:
		if len(sentence) > 0:
			print sentence[0:100]
			blob = TextBlob(sentence)
			print blob.sentiment
			print "\n"

def analyze_literal(sentences):
	for sentence in sentences:
		print sentence
		blob = TextBlob(sentence)
		print blob.sentiment
		print "\n"

if __name__=="__main__":
	#Basic demo
	print "-------------BASIC LITERAL----------------------\n"
	sentences = ["UNC is the worst school in the world", "Some movies are long", "I love Duke University!"]
	analyze_literal(sentences)
	print "-------------FILES----------------------\n"
	file_names = ['NYTArticles.txt','NYTBlogArticles.txt']
	for file_name in file_names:
		print file_name
		analyze_file(file_name)
		