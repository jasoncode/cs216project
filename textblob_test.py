# -*- coding: utf-8 -*-
import csv
from textblob import TextBlob

def analyze_file(file_name, mode):
	with open('results.csv',mode) as csvfile:
		data_file = open(file_name,'r')
		sentences = []
		sentence = ""
		csv_writer = csv.writer(csvfile, delimiter=',', lineterminator = '\n')
		extension_pos = file_name.index('.')
		raw_file_name = file_name[:extension_pos]
		csv_writer.writerow([raw_file_name.upper(), raw_file_name.upper()])
		csv_writer.writerow(["Subjectivity", "Polarity"])
		for line in data_file:
			utf_line = line.decode("utf-8")
			ascii_line  =utf_line.encode("ascii","ignore")
			if 'ARTICLE' in ascii_line:
				sentences.append(sentence)
				sentence = ""
			else:
				sentence+= " " + ascii_line
		for sentence in sentences:
			if len(sentence) > 0:
				#print sentence[0:100]
				blob = TextBlob(sentence)
				(polarity, subjectivity) = blob.sentiment
				csv_writer.writerow([subjectivity, polarity])
				#print "\n"
		csv_writer.writerow(['',''])

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
			analyze_file(file_name, 'a') #Appends to all current versions
		
		