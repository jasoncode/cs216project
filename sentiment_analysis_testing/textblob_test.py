# -*- coding: utf-8 -*-
import csv
from textblob import TextBlob

#Removes extension and writes filename in upper case for write_csv_header
def process_file_name(filename):
	extension_pos = file_name.index('.')
	raw_file_name = file_name[:extension_pos]
	return [raw_file_name.upper(), raw_file_name.upper()]

#Performs textblob's sentiment analysis on the parameter sentence
def sentence_sentiment(sentence):
	blob = TextBlob(sentence)
	(polarity, subjectivity) = blob.sentiment
	return [subjectivity, polarity]

#Puts a line of the txt file into ascii format
def ascii_prepare(line):
	return line.decode("utf-8").encode("ascii","ignore")

#Writes the lines indicating what file it is and the sentiment features
def write_csv_header(csv_writer, file_name):
	csv_writer.writerow(process_file_name(file_name))
	csv_writer.writerow(["Subjectivity", "Polarity"]) 

#Performs sentiment analysis on a text file containing some number of articles and
#writes results to a csv file
def analyze_file(file_name, mode):
	with open('results.csv',mode) as csvfile:
		data_file = open(file_name,'r')
		sentences = []
		sentence = ""
		csv_writer = csv.writer(csvfile, delimiter=',', lineterminator = '\n')
		write_csv_header(csv_writer, file_name)
		for line in data_file:
			ascii_line = ascii_prepare(line)
			if 'ARTICLE' in ascii_line:
				sentences.append(sentence)
				sentence = ""
			else:
				sentence+= " " + ascii_line
		for sentence in sentences:
			if len(sentence) > 0:
				csv_writer.writerow(sentence_sentiment(sentence))

		csv_writer.writerow(['',''])

#Analyzes a given list of literal sentences to demonstrate textblob's capabilities
def analyze_literal(sentences):
	for sentence in sentences:
		print sentence
		blob = TextBlob(sentence)
		print blob.sentiment
		print "\n"

if __name__=="__main__":
	#Basic demo
	print "-------------BASIC LITERAL----------------------\n"
	sentences = ["UNC is the worst school in the world", "Some movies are long", "Why are hats?", "I love Duke University!", "The sky might be blue."]
	analyze_literal(sentences)
	print "-------------FILES----------------------\n"
	file_names = ['NYTArticles.txt','NYTBlogArticles.txt']
	first = True
	for file_name in file_names:
		print file_name
		if first:
			analyze_file(file_name, 'w') #Overwrites any old versions
			first = False
		else:
			analyze_file(file_name, 'a') #Appends to current version
		
		