# -*- coding: utf-8 -*-
import csv
from textblob import TextBlob
import os


NUM_SUMMARY_STATS = 4
SUMMARY_STATS = ['Mean', 'Absolute Mean', 'Median', 'Absolute Median']
ARTICLES = 500
LEN_ROWS = ARTICLES + NUM_SUMMARY_STATS + 2 #2 for buffer.
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

    return (subjectivities,polarities)

def compute_summary(subjectivities, polarities):
    if len(subjectivities) > 0:
        mean_row = [compute_mean(subjectivities), compute_mean(polarities)]
        abs_mean_row = [compute_mean(subjectivities),compute_mean([abs(p) for p in polarities])]
        median_row = [compute_median(subjectivities), compute_median(polarities)]
        abs_median_row = [compute_median(subjectivities), compute_median([abs(p) for p in polarities])]
        return [mean_row, abs_mean_row, median_row, abs_median_row]
    return [['',''],['',''],['',''],['','']]
  
def write_headers(writers, title):
     writers['source'].writerow([title.upper(), ''])
     writers['article'].writerow([title.upper(), 'Subjectivity','Polarity'])
     summary_header = [title]
     for stat in SUMMARY_STATS:
         summary_header.extend([stat, ' '])
     writers['summary'].writerow(summary_header)
     writers['summary'].writerow(['', 'Num_Articles'] + ['Subjectivity','Polarity']*NUM_SUMMARY_STATS)
     

def write_output(writers, source_rows, article_rows, summary_rows):
    for row in source_rows:
        writers['source'].writerow(row)
    for row in article_rows:
        writers['article'].writerow(row)
    for row in summary_rows:
        writers['summary'].writerow(row)

def process_files(title, file_names, writers):
        source_rows = [[''] for i in range(LEN_ROWS)]
        for i in range(NUM_SUMMARY_STATS):
            source_rows[LEN_ROWS-(NUM_SUMMARY_STATS-i)] = [SUMMARY_STATS[i]]

        article_rows = []
        summary_rows = []
        write_headers(writers, title)
       
        all_subj = []
        all_pol = []
        output = {'source':source_rows, 'article':article_rows, 'summary':summary_rows}

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
                for j in range(i+1, LEN_ROWS-NUM_SUMMARY_STATS-1):
                    source_rows[j].extend(['',''])
                
                #Prepare summary statistics to write to file_name
                summary = compute_summary(subjectivities, polarities)
                summary_flat = []
                for i in range(NUM_SUMMARY_STATS):
                    source_rows[LEN_ROWS+(i-NUM_SUMMARY_STATS)].extend(summary[i])
                    summary_flat.extend(summary[i])
                if len(subjectivities) > 5:
                    summary_rows.append([header_name, len(subjectivities)]+summary_flat)
                    

                
        source_rows.append([])
        summary_rows.append([])
        article_rows.append([])
        spaces = [' '] * ((4 * len(file_names) - 4) / 2 - 1) #Centering for the overall summary
        source_rows.append(spaces + ['', title + ' Summary'])
        summary = compute_summary(all_subj, all_pol)
        for i in range(NUM_SUMMARY_STATS):
            source_rows.append(spaces + [SUMMARY_STATS[i]] + summary[i])
            article_rows.append([SUMMARY_STATS[i]] + summary[i])

        source_rows.append([])
        summary_rows.append([])
        article_rows.append([])
        write_output(writers, source_rows, article_rows, summary_rows)
            
def make_writer(file_path):
    file = open(file_path, 'wb')
    writer = csv.writer(file, delimiter = ',')
    return writer

if __name__=="__main__":
    real_folder_path = '../Scraping/RealNews/'
    fake_folder_path = '../Scraping/FakeNews/'

    real_file_names = [real_folder_path + file_name for file_name in os.listdir(real_folder_path)]
    fake_file_names = [fake_folder_path + file_name for file_name in os.listdir(fake_folder_path)]
    
    source_path = ('source', make_writer('../Results/resuls_bysource.csv'))
    summary_path = ('summary',make_writer('../Results/results_source_summary.csv'))
    article_path = ('article', make_writer('../Results/results_byarticle.csv'))
    paths = [source_path, summary_path, article_path]

    writers = {path[0]:path[1] for path in paths}
    process_files('Real News', real_file_names, writers)   
    print ("On to fake news")
    process_files('Fake News', fake_file_names, writers) 
    