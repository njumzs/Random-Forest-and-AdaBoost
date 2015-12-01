#!/usr/bin/env python
#-*- coding=utf-8 -*-
#########################################################
#Author:    Zhanshuai Meng
#Email: nju.mzs@outlook.com
#Created:   1 Dec 2015
########################################################
import math
from collections import defaultdict

class Id3(object):
    def __init__(self, examples, label):
        self.examples = examples
        self.labels = labels

    def cal_entropy(self, examples):
        """
        examples save indexes of the self.examples
        """
        class_freq = defaultdict(dict)
        for example_index in examples:
            class_freq[label[example_index]] += 1.0
        example_num = len(examples)
        entropy_vlaue = 0
        for freq_value in class_freq.values():
            entropy_vlaue += (-freq_value/example_num)* math.log(freq_value/example_num,2)
        return entropy_vlaue
    def cal_gain(self, examples, attr):
        """
        attr is the index of the selected feature
        examples is the index of the self.examples
        """
        attr_freq = defaultdict(dict)
        for row_index in examples:
            example = self.examples[row_index]
            attr_freq[example[attr]] += 1.0
        examples_sum = sum(attr_freq.values())
        sum_subentropy = 0.0
        for attr_key in attr_freq.keys():
            attr_perc = attr_freq[attr_key]/examples_sum
            sub_examples = [example for example in examples if self.examples[example][attr] == attr_key]
            sum_subentropy += self.cal_entropy(sub_examples)

        return entropy(data) - sum_subentropy
    def get_best_attr(self,examples,attrs):
        """
        choose the best attribute based on gain or entropy
        attrs is the list of index of the alternative attributes
        """
        chosen_attr = None
        best_fit = 0.0
        for attr in attrs:
            fitness_value = fit_func(examples,attr)
            if(fitness_value>best_fit):
                best_fit =  fitness_value
                chosen_attr = attr
        return best_attr

    def decision_tree(self,examples,attr):
        """
        pass
        examplexs save the index list of the
        """
        example_instances = [self.examples[example] for example in examples]








