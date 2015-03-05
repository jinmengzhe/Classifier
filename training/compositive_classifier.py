'''
Created on 2014-11-25

@author: jinmengzhe
'''
from classifier import MIClassifier

class CompositiveClassifier(object):
    '''
    This class is just the encapsulation of MIClassifier. providing 2 classifier:
    B2c Classifier and Taobao Classifier.
    '''
    def __init__(self, b2c_smi_file, taobao_smi_file):
        self.__b2c_classifier = MIClassifier(b2c_smi_file + '.fc',  b2c_smi_file + '.lc', b2c_smi_file);
        self.__taobao_classifier = MIClassifier(taobao_smi_file + '.fc',  taobao_smi_file + '.lc', taobao_smi_file);
    
    def classify_by_feature_doc(self, feature_doc, is_b2c):
        if is_b2c:
            return self.__b2c_classifier.classify_by_feature_doc(feature_doc)
        return self.__taobao_classifier.classify_by_feature_doc(feature_doc)


if __name__ == '__main__':
    pass
