# -*- coding: utf-8 -*-
'''
Created on 2014-11-10

@author: jinmengzhe
'''

import sys
import time
import math

from feature_util import parse_label_and_feature_count_dict
from feature_util import parse_label_url_title_property_features

class MILoader(object):
    def __init__(self, fc_file_path, lc_file_path, smi_file_path):
        self.__feature_count_dict = self.__load_word_count(fc_file_path)
        self.__label_count_dict = self.__load_word_count(lc_file_path)
        self.__label_total_count = int(self.__label_count_dict['__total_count__']) * 1.0
        
        self.__label_feature_weight = self.__compute_label_feature_weight(smi_file_path)
        self.__feature_weight = self.__compute_feature_weight()
        self.__feature_labellist = self.__compute_feature_labels_dict()
    
    def get_smi_result(self):
        return self.__label_feature_weight, self.__feature_weight, self.__feature_labellist
    
    def print_smi_result(self):
        print '__label_feature_weight:\n'
        for label, feature_weight_dict in self.__label_feature_weight.items():
            for feature, weight in feature_weight_dict.items():
                print str(label) + '\t' + feature + '\t' + str(weight)
            print '\n'
            
        print '\n__feature_weight:\n'
        for feature, weight in self.__feature_weight.items():
            print feature + '\t' + str(weight)
        
        print '\n__feature_labellist:\n'
        for feature, label_list in self.__feature_labellist.items():
            ss = feature + '\t'
            for label in label_list:
                ss += str(label) + ','
            print ss
        
            
            
    def __load_word_count(self, file_path):
        word_count_dict = {}
        reader = open(file_path, 'r')
        while True:
            line = reader.readline()
            if not line:
                break
            word_count = line.split('\t')
            if len(word_count) != 2:
                continue
            word = word_count[0]
            count = word_count[1]
            word_count_dict[word] = count
        reader.close()
        return word_count_dict
    
    def __compute_feature_weight(self):
        feature_weight = {}
        max_weight = None
        for feature, count in self.__feature_count_dict.items(): 
            feature_weight[feature] = math.log(int(count) / self.__label_total_count)
            if max_weight == None or max_weight > feature_weight[feature]:
                max_weight = feature_weight[feature]
        ### normalize to max_weight
        for feature, weight in feature_weight.items():
            feature_weight[feature] = weight / max_weight * -1
        return feature_weight
    
    def __compute_label_feature_weight(self, smi_file_path):
        label_feature_weight = {}
        smi_reader = open(smi_file_path, 'r')
        while True:
            line = smi_reader.readline()
            if not line:
                break
            label, label_feature_count_dict = parse_label_and_feature_count_dict(line)
            label_count = int(self.__label_count_dict[label])
            ## recompute label_feature_count_dict
            for feature, label_feature_count in label_feature_count_dict.items():
                feature_count = int(self.__feature_count_dict[feature])
                p_weight = self.__label_total_count * int(label_feature_count) / (label_count) * feature_count
                label_feature_count_dict[feature] = math.log(p_weight)
            # finish 1 label
            label_feature_weight[label] = label_feature_count_dict
        smi_reader.close()
        return label_feature_weight
    
    ## compute an inverted index from feature-->labels, to improve the efficiency of classify
    ## it's used to candidate a possible label to compute when classify
    def __compute_feature_labels_dict(self):
        feature_labellist_dict = {}
        for label, feature_weight_dict in self.__label_feature_weight.items():
            for feature in feature_weight_dict.keys():
                if not feature_labellist_dict.has_key(feature):
                    feature_labellist_dict[feature] = []
                labellist = feature_labellist_dict[feature]
                labellist.append(label)
        return feature_labellist_dict



class MIClassifier(object):
    def __init__(self, fc_file_path, lc_file_path, smi_file_path):
        self.__stop_words = ['淘宝', '代购', '现货', '促销', '特价', '清仓']
        self.__gender_words = ['男', '女', '童']
        self.__only_words = ['幼儿', '儿童', '男士', '女式', '男', '女']
      
        self.__loader = MILoader(fc_file_path, lc_file_path, smi_file_path)
        self.__label_feature_weight, self.__feature_weight, self.__feature_labellist = self.__loader.get_smi_result()
        
        #self.__loader.print_smi_result()
    
    ### compute score between feature_doc and label
    def compute_score_between(self, feature_doc, label):
        ### product_weight
        total_words = 0
        for feature_list in feature_doc.values():
            total_words += len(feature_list)
        if total_words <= 4:
            product_weight = 2
        else:
            product_weight = math.log(total_words, 2)
        # compute score
        score = 0
        feature_weight = self.__label_feature_weight[label]
        for property_field, feature_list in feature_doc.items():
            for feature in feature_list:
                feature_score = 0
                if feature_weight.has_key(feature):
                    if feature in self.__stop_words:
                        continue
                    feature_score = feature_weight[feature]                                                                       
                else:   
                    if self.__feature_weight.has_key(feature):
                        feature_score = self.__feature_weight[feature]
                if feature.find('孕妇') >= 0 or feature.find('婴幼儿') >= 0:
                        feature_score *= 4.8
                if property_field == 'product':                            
                    feature_score = feature_score * product_weight 
                elif property_field == 'brand':
                    feature_score = feature_score * product_weight 
                elif property_field == 'gender' and (feature in self.__gender_words):
                    feature_score = feature_score * product_weight
                elif property_field == 'only':
                    feature_score = feature_score * product_weight                         
                    if feature in self.__only_words:
                        feature_score *= 2
                elif property_field == 'seg_nr':                            
                    feature_score = feature_score * product_weight / 2                      
                        
                score += feature_score
        ## return score
        return score
        
        
    def select_labels(self, feature_doc):
        selected_labels = []
        for feature_list in feature_doc.values():
            for feature in feature_list:
                if self.__feature_labellist.has_key(feature):
                    label_list = self.__feature_labellist[feature]
                    selected_labels += label_list
        return set(selected_labels)   ### remove duplicate
        
    ## feature_doc:{property: [feature1, feature2,,,]}
    ###
    def classify_by_feature_doc(self, feature_doc):
        ### classfiy by score
        result_label = None
        result_score = None
        selected_labels = self.select_labels(feature_doc)
        for label in selected_labels:
        #for label in self.__label_feature_weight.keys():
            score = self.compute_score_between(feature_doc, label)
            if result_score == None or score > result_score :
                result_label = label
                result_score = score
        if not result_score > 0.0:
            return -1
        return result_label


def dict_key_add(mydict, key):
    if not mydict.has_key(key):
        mydict[key] = 0
    mydict[key] += 1
    
if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print 'Usage: python classifier.py [smi_file] [test_fs_file]'
        sys.exit()
    smi_file_path = sys.argv[1]
    test_fs_file_path = sys.argv[2]
    fc_file_path = smi_file_path + '.fc'
    lc_file_path = smi_file_path + '.lc'
    statistic_file = test_fs_file_path + '.statistic'
    statistic_error_file = test_fs_file_path + '.classify_error'
    print time.localtime()
    classifier = MIClassifier(fc_file_path, lc_file_path, smi_file_path)
    print 'finish load MIClassifier'
    print time.localtime()
    
    reader = open(test_fs_file_path, 'r')
    statistic_writer = open(statistic_file, 'w')
    error_writer = open(statistic_error_file, 'w')
    label_totalcount_dict = {}
    label_correctcount_dict = {}
    error_lines = []
    
    LINE_SIZE = 1000000
    while True:
        ## read as more as 10w lines
        print 'start to read as more as ' + str(LINE_SIZE) + ' lines'
        print time.localtime()
        line_list = []
        while True:
            line = reader.readline()
            if not line:
                break
            line_list.append(line)
            if len(line_list) == LINE_SIZE:
                break
        print 'start to classify ' + str(LINE_SIZE) + ' lines'
        print time.localtime()
        ## classify 10w lines
        if len(line_list) > 0:
            for line in line_list:
                label, url, title, property_features = parse_label_url_title_property_features(line)
                result = classifier.classify_by_feature_doc(property_features)
                if str(label) == str(result):
                    dict_key_add(label_totalcount_dict, label)
                    dict_key_add(label_correctcount_dict, label)
                else:
                    error_lines.append(str(label) + '\t' + str(result) + '\t' + title + '\t' + url)
                    dict_key_add(label_totalcount_dict, label)       
        else:
            break
    ### write error-statistic file
    for error_line in error_lines:
        error_writer.write(error_line + '\n')
    error_writer.flush()
    error_writer.close()
    ### write statistic file
    statistic_writer.write('label\t' + 'total_count\t' + 'correct_count\t' + 'accuracy\n')
    all_count = 0
    all_correct = 0
    for label, total_count in label_totalcount_dict.items():
        correct_count = 0
        if label_correctcount_dict.has_key(label):
            correct_count = label_correctcount_dict[label]
        accuracy = 1.0 * correct_count / total_count
        statistic_writer.write(str(label) + '\t' + str(total_count) + '\t' + str(correct_count) + '\t' + str(accuracy) + '\n')
        
        all_count += total_count
        all_correct += correct_count
    
    all_accuracy = 1.0 * all_correct / all_count
    statistic_writer.write(str(all_count) + '\t' + str(all_correct) + '\t' + str(all_accuracy))
    statistic_writer.flush()
    statistic_writer.close()
    
    print time.localtime()
    print 'finish~'
    