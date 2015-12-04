#!/usr/bin/env python
#-*- coding=utf-8 -*-
##################################################################################
#Author:    Zhanshuai Meng
#Email: nju.mzs@outlook.com
#Created:   3 Dec 2015
##################################################################################

import random
from ID3 import Id3

class RandomForests(object):
    def __init__(self,examples,labels):
        self.examples = examples
        self.labels = labels
        self.trees = []
    def sample_examples(self,k=len(self.examples)):
        """
        Return example instances, not index list
        """
        rtn_examples = []
        rtn_labels = []
        for i in range(k):
            rtn_examples.append(self.examples[random.randint(0,k-1)])
            rtn_labels.append(self.examples[random.randint(0,k-1)])
        return rtn_examples,rtn_labels

    def attributes_gen(self,q):
        """
        q is the number of selected attributes by random forests
        """
        rtn_attributes = []
        #Choose q attributes
        for i in range(q):
            attr = None
            while (not attr in rtn_attribute):
                attr = random.ranint(0,len(self,examples[0]))
            rtn_attributes.append(attr)
        return rtn_attributes
    def create_forests(self,tree_num):
        """
        Create tree_num decision trees
        """
        for i in range(treenum):
            examples, labels = self.sample_examples()
            id3 = Id3(examples, labels)
            self.trees.append(id3.decision_tree(range(len(examples)),range(len(labels)),self.attributes_gen))










