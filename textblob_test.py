from textblob import TextBlob

if __name__=="__main__":
	#sentences = ["UNC is the worst school in the world", "Some movies are long", "I love Duke University!"]
	file = open('articleText.txt','r')
	sentences = []
	for line in file:
		sentences.append(line)
	for sentence in sentences:
		print sentence
		sentence.decode('utf-8').encode('ascii')
		blob = TextBlob(sentence)

		print blob.sentiment