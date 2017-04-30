import sys
import csv
import os
import codecs

def make_txt(filename):
    with open(filename, 'r') as csvfile:
        rows = csv.reader(csvfile)
        current_source_name = ""
        file = open("NOT_REAL_FILE","w")
        for row in rows:
            source_name = row[1].replace('.','-')
            text = row[3]
            if source_name != current_source_name:
                file.close()
                file = open("./FakeNews/Kaggle-" + source_name + "Articles.txt","w") #"Kaggle" in front will make all files easier to delete if necessary
                current_source_name = source_name
            file.write("ARTICLE\n")
            file.write("\n")
            file.write(text)
            file.write("\n")
        file.close()
        os.remove("NOT_REAL_FILE")
if __name__ == '__main__':
     filename = sys.argv[1]
     make_txt(filename)