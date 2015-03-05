'''
Created on 2014-11-14

@author: jinmengzhe
'''
import sys
from sys import argv

error_case_file = 'error_case'

def get_error_urls():
    urls = []
    error_reader = open(error_case_file, 'r')
    while True:
        line = error_reader.readline()
        if not line:
            break
        items = line.split('\t')
        if len(items) > 1:
            urls.append(items[0].rstrip())
    error_reader.close()
    return urls

if __name__ == '__main__':
 
    if (len(sys.argv) != 2):
        print 'error'
        sys.exit()
    fs_all_file = argv[1]
    result_file = fs_all_file + '.except'
    
    error_url_list = get_error_urls()
    
    reader_fs_all = open(fs_all_file, 'r')
    result_writer = open(result_file, 'w')
    while True:
        line = reader_fs_all.readline()
        if not line:
            break
        items = line.split("--#####--")
        url = items[1]
        if url not in error_url_list:
            result_writer.write(line)
            
    reader_fs_all.close()
    result_writer.flush()
    result_writer.close()
    