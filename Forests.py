#!/usr/bin/env python
#-*- coding=utf-8 -*-
##################################################################################
#Author:    Zhanshuai Meng
#Email: nju.mzs@outlook.com
#Created:   3 Dec 2015
##################################################################################

import random
from ID3 import Id3
import math
from collections import defaultdict
from collections import Counter
import sys   
sys.setrecursionlimit(1000000)
class RandomForests(object):
    def __init__(self,examples,labels):
        self.examples = examples
        self.labels = labels
    def sample_examples(self,prop=1.0):
        """
        Return example instances, not index list
        """
        k=int(len(self.examples)*prop)
        rtn_examples = []
        rtn_labels = []
        for i in range(k):
            index = random.randint(0,k-1)
            rtn_examples.append(self.examples[index])
            rtn_labels.append(self.labels[index])
        return rtn_examples,rtn_labels

    def attributes_gen(self,q):
        """
        q is the number of selected attributes by random forests
        """
        rtn_attributes = []
        print "q ",q
        #Choose q attributes
        for i in range(int(q)):
            attr = None
            while (attr in rtn_attributes or (not attr)):
                attr = random.randint(0,len(self.examples[0])-1)
            rtn_attributes.append(attr)
        return rtn_attributes
    def create_forests(self,tree_num,testing_data,prop=0.5):
        """
        Create tree_num decision trees
        """
        results = []
        for i in range(tree_num):
            examples, labels = self.sample_examples(prop)
            id3 = Id3(examples, labels)
            tree = id3.decision_tree(range(len(examples)),range(len(self.examples[0])),math.log(len(self.examples[0]),2)+1)
            results.append(id3.get_class_labels(testing_data,tree))
        return results

    def conduct(self,testing_data,testing_label,prop=1.0,tree_num=2000):
        results = self.create_forests(tree_num,testing_data,prop)
        ensemble_results = defaultdict(list)
        for labels in results:
            for index, label in enumerate(labels):
                ensemble_results[index].append(label)
        labels = []
        for key in ensemble_results.keys():
            counter = dict(Counter(ensemble_results[key]))
            sort_counter  = sorted(counter.items(),key=lambda d:d[1],reverse=1)
            labels.append(sort_counter[0][0])
        com_result = [labels[i]==testing_label[i] for i in range(len(labels))]
        accurate_rate = com_result.count(True)*1.0/len(testing_label)
        return accurate_rate, labels





















