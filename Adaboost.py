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
from ID3 import Id3
from collections import defaultdict


class Ada(object):
    def __init__(self, examples, labels):
        """
        examples save the list of example instances
        labels represent the labels of  corresponding instances
        """
        self.examples = examples
        self.labels = labels
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
            rtn_records.append(choice(examples, p=weights))
        return rtn_records

    def get_base_class(self,classifier, prop):
        """
        classifier is the base classifier
        prop is the proportion to sample for the foundation of model
        """
        examples = self.examples[:]
        labels = self.labels[:]
        sample_examples = self.weighted_sample(prop)
        sample_labels  = [self.labels[index] for index in sample_examples]
        base_classifier = classifier(sample_examples,sample_labels)
        attributes = range(len(self.examples[0]))
        tree = base_classifier.decision_tree(sample_examples,attributes)
        results = base_classifier.get_class_labels(examples,tree)
        flag = [labels[i]==results[i] for i in range(len(results))]
        return flag,results
    def get_error_rate(self,flag):
        count = flag.count(False)
        return 1.0*count/len(flag)

    def adaboost(classifier,T,prop=0.3):
        """
        T is the num of iteration
        """
        result_label = []
        example_length = len(self.examples)
        iter_num = 0
        for i in range(T):
            flag,results = self.get_base_class(classifier,prop)
            error_rate = self.get_error_rate(flag)
            result_label = [result_label[i]+error_rate*results[i] for i in range(len(results))]
            result_rate.append(error_rate)
            result_label.append(results)
            a = 1/2*math.log((1-error_rate)/error_rate)
            for j in range(example_length):
                if flag[i]:
                    self.weights[j] *= math.exp(a)
                else:
                    self.weights[j] *= math.exp(-a)
            wights_sum = sum(self.weights)
            self.weights = [weight/weight_sum for weight in self.weights]
            iter_num += 1
            if (error_rate==0) or (error_rate>=0.5):
                break
        result_label = [result_label[i]*1.0/iter_num for i in range(len(result_label))]
        for i in range(len(result_label)):
            if result_label[i]<0:
                result_label[i] = -1
            else:
                result_label[i] = 1
        return result_label
