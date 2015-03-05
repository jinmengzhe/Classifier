# -*- coding: utf-8 -*-
'''
Created on 2014-11-7

@author: jinmengzhe
'''

import sys

def load_book_cat_list(tag_map_path):
    book_cat_list = []
    reader = open(tag_map_path, 'r')
    while True:
        line = reader.readline()
        if not line :
            break
        line = line.rstrip('\r\n\t ')
        arr = line.split('\t')
        cat3 = arr[0]
        cat1 = arr[2]
        if cat1 == '41':
            book_cat_list.append(cat3)
    reader.close()
    return book_cat_list

def generate_train_set(in_file_path, out_file_path, tag_map_path):
    book_cat_list = load_book_cat_list(tag_map_path);
    reader = open(in_file_path, 'r')
    writer = open(out_file_path, 'w')
    while True:
        line = reader.readline()
        if not line:
            break;
        items = line.split('|||')
        label = items[9]
        title = items[2]
        url = items[1]
        goods_id = items[0]
        if label == '-1' or label == '3841' or label in book_cat_list:
            continue
        data = url + '\t' + goods_id + '\t' + title + '\t' + label + '\n'
        writer.write(data)
    reader.close()
    writer.close()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: python generate_ts.py [b2c_train_set.data] [b2c_train_set.ts] [tag_map_file]'
        sys.exit()
    in_data = sys.argv[1]
    out_ts = sys.argv[2]
    tag_map_file = sys.argv[3]
    generate_train_set(in_data, out_ts, tag_map_file)
    print 'OK'