import os

if __name__ == '__main__':
    real_folder_path = '../Scraping/RealNews/'
    fake_folder_path = '../Scraping/FakeNews/'
    real_file_names = [real_folder_path + file_name for file_name in os.listdir(real_folder_path)]
    fake_file_names = [fake_folder_path + file_name for file_name in os.listdir(fake_folder_path)]
    real_file = open(real_folder_path + "all_real_news.txt","w")
    fake_file = open(fake_folder_path + "all_fake_news.txt","w")
    for file_name in real_file_names:
        file = open(file_name, 'r')
        for line in file:
            if line.strip() != 'ARTICLE':
                real_file.write(line)
    i = 0
    for file_name in fake_file_names:
        i += 1
        
        file = open(file_name, 'r')
        for line in file:
            if line.strip() != 'ARTICLE':
                fake_file.write(line)
    print i
                