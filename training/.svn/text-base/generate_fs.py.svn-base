# -*- coding: utf-8 -*-
'''
Created on 2014-11-9

@author: mengzhejin
'''

import sys
import time
sys.path.append('../segment/lib/')
from word_seg import segment
from feature_util import join_feature_string

class FeatureParser(object):     
    def __init__(self, seg_path='/data/jinmengzhe/myclassify/segment'):
        self.gender_male = '男'
        self.gender_female = '女' 
        self.gender_child = '童'
        self.seg = segment(seg_path)
    
    def check_gender(self, word):
        if word.find(self.gender_male) >= 0:
            return self.gender_male
        elif word.find(self.gender_female) >= 0:
            return self.gender_female     
        if word.find(self.gender_child) >= 0:
            return self.gender_child
        return None
        
    def parse_feature(self, title, url, label='0'):
        oringin_title = title
        title = title.decode('utf8', 'ignore').encode('gbk', 'ignore')
        word_tag_list = self.seg.get_word_tag(title)    
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
                gender = self.check_gender(word)
                if gender != None:
                    feat_doc['gender'] = [gender]
        if len(feat_doc) <= 0:
            return None
        return join_feature_string(label, url, oringin_title, feat_doc) + '\n'
    
    def parse_feature_set(self, ts_path, fs_path):
        reader = open(ts_path, 'r')
        writer = open(fs_path, 'w')
        while True:
            line = reader.readline()
            if not line :
                break
            line = line.rstrip('\r\n\t ')
            items = line.split('\t')
            if (len(items) != 4):
                print '[ERROR]--parse_feature_set: len(items)=' + str(len(items)) + 'line=' + line
                continue
            url = items[0]
            #goods_id = items[1]
            title = items[2]
            label = items[3]
            ss = self.parse_feature(title, url, label)
            if ss == None:
                print '[ERROR]--parse_feature_set: parse_feature() return None,line=' + line
                continue         
            writer.write(ss)
        reader.close()
        writer.close()
       
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: python generate_fs.py [ts_file] [fs_file] [seg_path]'
        sys.exit()
    ts_file = sys.argv[1]
    fs_file = sys.argv[2]
    seg_path = sys.argv[3]
    
    print time.localtime()
    parser = FeatureParser(seg_path)
    f = parser.parse_feature_set(ts_file, fs_file)
    print time.localtime()
    print 'OK'