# -*- coding: utf-8 -*-
import csv
from textblob import TextBlob

LEN_ROWS = 110
SUMMARY_STATS = 3
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
        
#Performs sentiment analysis on a text file containing some number of articles 
def analyze_file(file_name):
    
    data_file = open(file_name,'r')
    sentences = []
    subjectivities = []
    polarities = []
    sentence = ""
      
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
           
    return (subjectivities,polarities)

def compute_summary(subjectivities, polarities):
    mean_row = ['mean',compute_mean(subjectivities), compute_mean(polarities)]
    abs_mean_row = ['Absolute mean', compute_mean(subjectivities),compute_mean([abs(p) for p in polarities])]
    median_row = ['median', compute_median(subjectivities), compute_median(polarities)]
    return [mean_row, abs_mean_row, median_row]

def process_files(csv_writer, file_names, title):
        rows = [[] for i in range(LEN_ROWS)]
        csv_writer.writerow(['',title.upper(), ''])
        all_subj = []
        all_pol = []
        for file_name in file_names:
            #Prepare header
            rows[0].extend(['',process_file_name(file_name),''])
            rows[1].extend(["","Subjectivity", "Polarity"]) 
            
            #Compute sentiment analysis
            (subjectivities, polarities) = analyze_file(file_name) 
            
            all_subj.extend(subjectivities)
            all_pol.extend(polarities)
            
            #Prepare to write to file
            for i in range(2,min(LEN_ROWS-SUMMARY_STATS,2+len(subjectivities))):
                rows[i].extend(["", subjectivities[i-2], polarities[i-2]])
            for j in range(i+1, LEN_ROWS-SUMMARY_STATS):
                rows[j].extend(['','',''])
            
            #Prepare summary statistics to write to file
            summary_rows = compute_summary(subjectivities, polarities)
            for i in range(len(summary_rows)):
                rows[LEN_ROWS+(i-3)].extend(summary_rows[i])
                
            for row in rows:
                row.append('') #Spacing 
                
        rows.append([])
        spaces = [' '] * ((4 * len(file_names) - 4) / 2) #Centering for the overall summary
        rows.append(spaces + ['', title + ' Summary'])
        summary_rows = compute_summary(all_subj, all_pol)
        for row in summary_rows:
            rows.append(spaces + row)

        rows.append([])

        for row in rows:
            csv_writer.writerow(row)
        

if __name__=="__main__":
    folder_path = '../Scraping/'
    extension = '.txt'
    real_names = ['NYTPoliticalArticles','NewsExaminerArticles', 'NYTNationalArticles', 'NYTPoliticalArticles']
    fake_names = ['NYTNationalArticles']
    real_file_names = [folder_path + name + extension for name in real_names]
    fake_file_names = [folder_path + name + extension for name in fake_names]
    with open('results.csv','w') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', lineterminator = '\n')
        process_files(csv_writer, real_file_names, 'Real News')
        process_files(csv_writer, fake_file_names, 'Fake News')
      