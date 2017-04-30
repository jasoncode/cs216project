# -*- coding: utf-8 -*-
import csv
from textblob import TextBlob
import os

LEN_ROWS = 505
SUMMARY_STATS = 3
SIGNAL = "CS216 Group 6"

#Removes extension and writes filename in upper case for write_csv_header
def process_file_name(file_name):
    name_start = max(file_name.rfind('\\') , file_name.rfind('/'), file_name.rfind('Kaggle') + len('Kaggle'))
    extension_pos = file_name.rfind('Articles.')
    raw_file_name = file_name[name_start+1:extension_pos]
    return raw_file_name.upper()

#Puts a line of the txt file_name into ascii format
def ascii_prepare(line):

    try:
        final_line = line.decode("utf-8").encode("ascii","ignore")
    except:
        final_line = SIGNAL
    return final_line

def compute_mean(vals):
    return sum(vals)*1.0/len(vals)

def compute_median(vals):
    vals.sort()
    middle = len(vals)/2
    if len(vals) % 2 == 0:
        return (vals[middle] + vals[middle-1])/2.0
    else:
        return vals[middle] #Truncates to an int
        
#Performs sentiment analysis on a text file_name containing some number of articles 
def analyze_file(file_name):
    data_file = open(file_name,'r')
    sentences = []
    subjectivities = []
    polarities = []
    sentence = ""
    success = True
    for line in data_file:
        ascii_line = ascii_prepare(line)
        if 'ARTICLE' in ascii_line:
            if success:
                sentences.append(sentence)
            sentence = ""
            success = True
        elif ascii_line == SIGNAL:
            success = False
        else:
            sentence += ascii_line
    for sentence in sentences:
        if len(sentence.strip()) > 0:     
            blob = TextBlob(sentence)
            word_count = len(blob.words)
            if word_count > 50: 
                (polarity, subjectivity) = blob.sentiment
                subjectivities.append(subjectivity)
                polarities.append(polarity)
                if subjectivity == 1:
                    print sentence
    return (subjectivities,polarities)

def compute_summary(subjectivities, polarities):
    if len(subjectivities) > 0:
        mean_row = [compute_mean(subjectivities), compute_mean(polarities)]
        abs_mean_row = [compute_mean(subjectivities),compute_mean([abs(p) for p in polarities])]
        median_row = [compute_median(subjectivities), compute_median(polarities)]
        return [mean_row, abs_mean_row, median_row]
    return [['',''],['',''],['','']]
  

def process_files(by_source_writer, by_article_writer, file_names, title):
        source_rows = [[''] for i in range(LEN_ROWS)]
        source_rows[LEN_ROWS-3] = ['Mean']
        source_rows[LEN_ROWS-2] = ['Abs Mean']
        source_rows[LEN_ROWS-1] = ['Median']
        article_rows = []
        by_source_writer.writerow([title.upper(), ''])
        by_article_writer.writerow([title.upper()])
        all_subj = []
        all_pol = []

        for file_name in file_names:
            #Compute sentiment analysis
            (subjectivities, polarities) = analyze_file(file_name) 
            if len(subjectivities) > 0:
                #Prepare header
                header_name = process_file_name(file_name)
                source_rows[0].extend([header_name,''])
                source_rows[1].extend(['Subjectivity', 'Polarity']) 
            
                all_subj.extend(subjectivities)
                all_pol.extend(polarities)
                
                i = 1
                #Prepare to write to file_name
                for i in range(2,2+len(subjectivities)):
                    source_rows[i].extend([subjectivities[i-2], polarities[i-2]])
                    article_rows.append([header_name, subjectivities[i-2], polarities[i-2]])
                for j in range(i+1, LEN_ROWS-SUMMARY_STATS-1):
                    source_rows[j].extend(['',''])
                
                #Prepare summary statistics to write to file_name
                summary_rows = compute_summary(subjectivities, polarities)
                for i in range(SUMMARY_STATS):
                    source_rows[LEN_ROWS+(i-3)].extend(summary_rows[i])
                    

                
        source_rows.append([])
        spaces = [' '] * ((4 * len(file_names) - 4) / 2) #Centering for the overall summary
        source_rows.append(spaces + ['', title + ' Summary'])
        summary_rows = compute_summary(all_subj, all_pol)
        for row in summary_rows:
            source_rows.append(spaces + row)
        source_rows.append([])

        for row in source_rows:
            by_source_writer.writerow(row)
        for row in article_rows:
            by_article_writer.writerow(row)

if __name__=="__main__":
    real_folder_path = '../Scraping/RealNews/'
    fake_folder_path = '../Scraping/FakeNews/'

    real_file_names = [real_folder_path + file_name for file_name in os.listdir(real_folder_path)]
    fake_file_names = [fake_folder_path + file_name for file_name in os.listdir(fake_folder_path)]
    by_source_file = open('../Results/resuls_bysource.csv','w')
    by_article_file = open('../Results/results_byarticle.csv','w')
    source_csv_writer = csv.writer(by_source_file, delimiter=',', lineterminator = '\n')
    article_csv_writer = csv.writer(by_article_file, delimiter=',', lineterminator = '\n')
    process_files(source_csv_writer, article_csv_writer, real_file_names, 'Real News')   
    print ("On to fake news")
    process_files(source_csv_writer, article_csv_writer, fake_file_names, 'Fake News')  
    