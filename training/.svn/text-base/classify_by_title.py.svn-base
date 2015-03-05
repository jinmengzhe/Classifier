# -*- coding: utf-8 -*-
'''
Created on 2014-11-17

@author: jinmengzhe

just a test case, used to screening a special case.

'''
import sys
import os

sys.path.append('../segment/lib/')
from word_seg import segment
from classifier import MIClassifier


def check_gender(word):
    if word.find('男') >= 0:
        return '男'
    elif word.find('女') >= 0:
        return '女'     
    if word.find('童') >= 0:
        return '童'
    return None

###  This is copied from generate_fs.py
###  so when this original method changed in generate_fs.py, remember to change here
def parse_feature(seg, title):
    title = title.decode('utf8', 'ignore').encode('gbk', 'ignore')
    word_tag_list = seg.get_word_tag(title)    
    feat_doc = {}
    gender = None
    for w in word_tag_list:
        ##word           
        if len(w[0].rstrip()) <= 0 or w[1] == 'w':
            continue
        word = w[0].decode('gbk', 'ignore')
        ##f
        if w[1].startswith('o_'):
            f = w[1].split('_')[-1]            
        else:
            f = 'seg_' + w[1]
            if len(word) == 1:  # delete 1 length word
                continue
        ## f-->wordlist
        word = word.encode('utf8', 'ignore')
        if not feat_doc.has_key(f):
            feat_doc[f] = []
        if word not in feat_doc[f]:
            feat_doc[f].append(word)
        ## if add gender
        if gender == None:
            gender = check_gender(word)
            if gender != None:
                feat_doc['gender'] = [gender]
    if len(feat_doc) <= 0:
        return None
    return feat_doc

def print_propterty_wordlist(property_field, word_list):
    result = property_field + '\t['
    for word in word_list:
        result += word + ','
    result += ']'
    print result
    

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: python classify_by_title [smi_file_path] [title]"
        sys.exit()
    smi_file_path = sys.argv[1]
    fc_file_path = smi_file_path + '.fc'
    lc_file_path = smi_file_path + '.lc'
    title = sys.argv[2]
    
    seg = segment('/data/jinmengzhe/myclassify/segment')
    classifier = MIClassifier(fc_file_path, lc_file_path, smi_file_path)
    
    feat_doc = parse_feature(seg, title)
    for property_field, word_list in feat_doc.items():
        print_propterty_wordlist(property_field, word_list)
        
    result = classifier.classify_by_feature_doc(feat_doc)
    print 'classify_result=' + str(result)
    
    