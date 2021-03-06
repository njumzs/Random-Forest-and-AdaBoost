#!/usr/bin/env python
#-*- coding=utf-8 -*-
#######################################################
#Author:    Zhanshuai Meng
#Email: nju.mzs@outlook.com
#Created:   4 Dec 2015
#Description:
#######################################################
import math
import numpy as np
from numpy.random import choice
#from ID3 import Id3
from collections import defaultdict
import ID3


class Ada(object):
    def __init__(self, examples, labels,flags):
        """
        examples save the list of example instances
        labels represent the labels of  corresponding instances
        """
        self.examples = examples
        self.labels = labels
        self.flags = flags 
        self.weights = [1.0/len(examples)]*len(examples)
    def weighted_sample(self, prop):
        """
        prop is the proportion to sample
        """
        examples = range(len(self.examples))
        weights = self.weights[:]
        sample_length = int(len(examples)*prop)
        rtn_records = []
        for i in range(sample_length):
            rtn_records.append(int(choice(examples, p=weights)))
        return rtn_records

    def get_base_class(self,classifier,testing_set, prop=1.0):
        """
        classifier is the base classifier
        prop is the proportion to sample for the foundation of model
        """
        examples = self.examples[:]
        labels = self.labels[:]
        sample_examples_index = self.weighted_sample(prop)
        sample_labels  = [self.labels[index] for index in sample_examples_index]
        sample_examples  = [self.examples[index] for index in sample_examples_index]
        base_classifier = classifier(sample_examples,sample_labels,self.flags)
        attributes = range(len(self.examples[0]))
        tree = base_classifier.decision_tree(range(len(sample_examples)),attributes)
        weight_results = base_classifier.get_class_labels(examples,tree)
        test_results = base_classifier.get_class_labels(testing_set,tree)
        weight_flag = [labels[i]==weight_results[i] for i in range(len(weight_results))]
        #test_flag = [testing_labels[i]==test_results[i] for i in range(len(test_results))]
        return test_results,weight_flag,weight_results

    def get_error_rate(self,flag):
        count = flag.count(False)
        return 1.0*count/len(flag)

    def adaboost(self,classifier,testing_set,testing_labels,T=10,prop=1.0):
        """
        T is the num of iteration
        """
        result_label = [0.0]*len(testing_set)
        example_length = len(self.examples)
        iter_num = 0
        for i in range(T):
            test_results,flag,results = self.get_base_class(classifier,testing_set,prop)
            com_flag = [test_results[j]==testing_labels[j] for j in range(len(test_results))]
            error_rate = self.get_error_rate(flag)
            a = 1.0/2*math.log((1-error_rate)*1.0/error_rate)
            result_label = [result_label[i]+a*test_results[i] for i in range(len(test_results))]
            for j in range(example_length):
                if flag[j]:
                    self.weights[j] *= math.exp(a)
                else:
                    self.weights[j] *= math.exp(-a)
            weights_sum = sum(self.weights)
            self.weights = [weight/weights_sum for weight in self.weights]
            iter_num += 1
            if (error_rate==0) or (error_rate>=0.5):
                break
        result_label = [result_label[i]*1.0/iter_num for i in range(len(result_label))]
        for i in range(len(result_label)):
            if result_label[i] < 0.0:
                result_label[i] = -1.0
            else:
                result_label[i] = 1.0
        return result_label
    def conduct(self,testing_set,testing_labels,T=100,prop=1.0):
        result_labels = self.adaboost(ID3.Id3,testing_set,testing_labels,T,prop)
        com_result = [result_labels[i]==testing_labels[i] for i in range(len(result_labels))]
        accurate_rate = com_result.count(True)*1.0/len(testing_labels)
        return accurate_rate, result_labels


