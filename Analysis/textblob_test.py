# -*- coding: utf-8 -*-

from textblob import TextBlob

if __name__=="__main__":
	#Basic demo
	print "-------------BASIC LITERAL----------------------\n"
	sentences = ["UNC is the worst school in the world", "Some movies are long", "Why are hats?", "Why are bears so stupid", "I love Duke University!", "The sky might be blue."]
	analyze_literal(sentences)
	for sentence in sentences:
		print sentence
		blob = TextBlob(sentence)
		print blob.sentiment
		print "\n"