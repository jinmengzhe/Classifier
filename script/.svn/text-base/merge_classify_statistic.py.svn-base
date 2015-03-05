'''
Created on 2014-11-13

@author: jinmengzhe
'''
import sys
import os

label_totalcount_dict = {}
label_correctcount_dict = {}

def dict_key_add(mydict, key, addcount):
    if not mydict.has_key(key):
        mydict[key] = 0
    mydict[key] += addcount

def merge_file(file_path):
    reader = open(file_path, 'r')
    reader.readline()
    while True:
        line = reader.readline()
        if not line:
            break
        items = line.split('\t')
        if len(items) != 4:
            continue
        label = items[0]
        total_count = int(items[1])
        correct_count = int(items[2])
        dict_key_add(label_totalcount_dict, label, total_count)
        dict_key_add(label_correctcount_dict, label, correct_count)
    reader.close()
    
    
    
if __name__ == '__main__':
    statistic_file_suffix = ".statistic"
    filelist = os.listdir(".")
    for statistic_file in filelist:
        if statistic_file_suffix in statistic_file:
            merge_file(statistic_file)
    ## all statistic
    writer = open("statistic.all", 'w')
    writer.write('label\t' + 'total_count\t' + 'correct_count\t' + 'accuracy\n')
    all_count = 0
    all_correct = 0
    for label, total_count in label_totalcount_dict.items():
        correct_count = 0
        if label_correctcount_dict.has_key(label):
            correct_count = label_correctcount_dict[label]
        accuracy = 1.0 * correct_count / total_count
        writer.write(str(label) + '\t' + str(total_count) + '\t' + str(correct_count) + '\t' + str(accuracy) + '\n')
        
        all_count += total_count
        all_correct += correct_count
    
    all_accuracy = 1.0 * all_correct / all_count
    writer.write(str(all_count) + '\t' + str(all_correct) + '\t' + str(all_accuracy))
    writer.flush()
    writer.close()
    
            