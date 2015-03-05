# -*- coding: utf-8 -*-
'''
Created on 2014-11-10

@author: jinmengzhe
'''
import sys
import time
from feature_util import parse_label_and_features
from feature_util import join_smi_string

class MultualInfoTask():
    def __init__(self, fs_input_file, smi_output_file):
        self.__fsReader = open(fs_input_file, 'r')
        self.__smiWriter = open(smi_output_file, 'w')
        self.__fcWriter = open(smi_output_file + '.fc', 'w')
        self.__lcWriter = open(smi_output_file + '.lc', 'w')
        ### indicators to statistic 
        self.__featue_count_dict = {}
        self.__label_count_dict = {}       
        self.__label_feature_count_dict = {}
        self.__total = 0
    
    def __close(self):
        self.__fsReader.close()
        self.__smiWriter.close()
        self.__fcWriter.close()
        self.__lcWriter.close()
    
    def __key_incr_in_dict(self, key, _dict):
        if _dict.has_key(key):
            _dict[key] += 1
        else:
            _dict[key] = 1
    
    def __write_fc_file(self):
        for feature, count in self.__featue_count_dict.items():
            self.__fcWriter.write(feature + '\t' + str(count) + '\n')
         
    def __write_lc_file(self):
        for label, count in self.__label_count_dict.items():
            self.__lcWriter.write(label + '\t' + str(count) + '\n')
        self.__lcWriter.write('__total_count__' + '\t' + str(self.__total) + '\n')
        
    def __write_smi_file(self):
        for label, feature_count_dict in self.__label_feature_count_dict.items():
            smi_string = join_smi_string(label, feature_count_dict)
            self.__smiWriter.write(smi_string + '\n')
       
    ## just use features and label
    def __handle_Record(self, label_and_features):
        label = label_and_features['label']
        features = label_and_features['features']
        
        # __label_count_dict
        self.__key_incr_in_dict(label, self.__label_count_dict)
        # __label_feature_count_dict
        if not self.__label_feature_count_dict.has_key(label):
            self.__label_feature_count_dict[label] = {}                
        temp_feature_count_dict = self.__label_feature_count_dict[label]
        # __featue_count_dict
        for feature in features:                           
            self.__key_incr_in_dict(feature, temp_feature_count_dict)               
            self.__key_incr_in_dict(feature, self.__featue_count_dict)
        # __total
        self.__total += 1
        
    def run_task(self):
        while True:
            line = self.__fsReader.readline()
            if not line:
                break
            line = line.rstrip('\r\n\t ')
            label_and_features = parse_label_and_features(line)
            if label_and_features == None:
                print '[ERROR]--label_and_features is None.line=' + line
                continue
            self.__handle_Record(label_and_features)
        
        print 'total fs record: ' + str(self.__total)
        self.__write_fc_file()
        self.__write_lc_file()
        self.__write_smi_file()
        self.__close()
    
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python mutual_info.py [b2c_train_set.fs] [b2c_train_set.smi]'
        sys.exit()
    fs_input_file = sys.argv[1]
    smi_output_file = sys.argv[2]
    
    print time.localtime()
    task = MultualInfoTask(fs_input_file, smi_output_file)
    task.run_task()
    print time.localtime()
    print 'finish MultualInfoTask~'