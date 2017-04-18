# -*- coding: utf-8 -*-
import csv
from textblob import TextBlob

#Removes extension and writes filename in upper case for write_csv_header
def process_file_name(file_name):
    name_start = max(file_name.rfind('\\') , file_name.rfind('/'))
    extension_pos = file_name.rfind('.')
    raw_file_name = file_name[name_start+1:extension_pos]
    return raw_file_name.upper()

#Puts a line of the txt file into ascii format
def ascii_prepare(line):
    return line.decode("utf-8").encode("ascii","ignore")

def compute_mean(vals):
    return sum(vals)*1.0/len(vals)

def compute_median(vals):
    vals.sort()
    middle = len(vals)/2
    if len(vals) % 2 == 0:
        return (vals[middle] + vals[middle-1])/2.0
    else:
        return vals[middle] #Truncates to an int
        
#Performs sentiment analysis on a text file containing some number of articles and
#writes results to a csv file
def analyze_file(file_name, mode):
    with open('results.csv',mode) as csvfile:
        data_file = open(file_name,'r')
        sentences = []
        subjectivities = []
        polarities = []
        sentence = ""
        csv_writer = csv.writer(csvfile, delimiter=',', lineterminator = '\n')
        
        #Write header for each new file
        csv_writer.writerow(['',process_file_name(file_name)])
        csv_writer.writerow(["","Subjectivity", "Polarity"]) 
        
        for line in data_file:
            ascii_line = ascii_prepare(line)
            if 'ARTICLE' in ascii_line:
                sentences.append(sentence)
                sentence = ""
            else:
                sentence+= " " + ascii_line
        for sentence in sentences:
            if len(sentence) > 0:
                blob = TextBlob(sentence)
                (polarity, subjectivity) = blob.sentiment
                subjectivities.append(subjectivity)
                polarities.append(polarity)
                csv_writer.writerow(["", subjectivity, polarity])
        
        csv_writer.writerow(['','',''])
        csv_writer.writerow(['mean',compute_mean(subjectivities), compute_mean(polarities)])
        csv_writer.writerow(['median', compute_median(subjectivities), compute_median(polarities)])
        csv_writer.writerow(['',''])



if __name__=="__main__":
    file_names = ['../Scraping/NYTPoliticalArticles.txt','../Scraping/NewsExaminerArticles.txt']
    first = True
    for file_name in file_names:
        if first:
            analyze_file(file_name, 'w') #Overwrites any old versions
            first = False
        else:
            analyze_file(file_name, 'a') #Appends to current version
        
         